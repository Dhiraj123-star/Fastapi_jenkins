import os
import requests
import logging
from fastapi import FastAPI, Depends
from dotenv import load_dotenv
from pymongo import MongoClient
from redis import Redis
from datetime import datetime, timedelta
from bson import ObjectId
import json

# Load environment variables
load_dotenv()

# Initialize FastAPI
app = FastAPI()

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Dependency to get API key securely
def get_weather_api_key():
    api_key = os.getenv("WEATHER_API_KEY")
    if not api_key:
        raise ValueError("Weather API key is missing. Set it in the .env file.")
    return api_key

# MongoDB connection setup
MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongo:27017")  # Default to Docker service name
client = MongoClient(MONGO_URI)
db = client.weather_db  # Database name
collection = db.weather_data  # Collection name

# Redis connection setup
REDIS_HOST = os.getenv("REDIS_HOST", "redis")  # Default to Docker service name
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))  # Default Redis port
redis_client = Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, decode_responses=True)

# Set cache expiry time (in seconds)
CACHE_EXPIRY = 300  # 5 minutes
MONGO_DATA_EXPIRY_MINUTES = 10  # Auto-delete records older than 10 minutes

# Utility to serialize MongoDB documents
def serialize_doc(doc):
    doc["_id"] = str(doc["_id"])  # Convert ObjectId to str
    return doc

# Cache Eviction: Remove old MongoDB records
def remove_old_mongo_data():
    expiry_time = datetime.utcnow() - timedelta(minutes=MONGO_DATA_EXPIRY_MINUTES)
    result = collection.delete_many({"timestamp": {"$lt": expiry_time}})
    if result.deleted_count > 0:
        logging.info(f"Cache Eviction: Removed {result.deleted_count} expired records from MongoDB.")

@app.get("/weather/")
def get_weather(city: str, api_key: str = Depends(get_weather_api_key)):
    """Fetches and stores the weather data for a given city, with Redis caching and eviction"""

    # Check Redis cache
    cached_data = redis_client.get(city)
    if cached_data:
        logging.info(f"Cache hit: Returning weather data for {city} from Redis")
        return json.loads(cached_data)

    # Check if the city data is already in MongoDB (cache eviction applied)
    remove_old_mongo_data()  # Remove stale data from DB before querying
    existing_data = collection.find_one({"city": city})
    
    if existing_data:
        logging.info(f"DB hit: Returning weather data for {city} from MongoDB")
        serialized_data = serialize_doc(existing_data)
        redis_client.setex(city, CACHE_EXPIRY, json.dumps(serialized_data))  # Cache for 5 minutes
        return serialized_data

    # Fetch from external Weather API
    logging.info(f"API call: Fetching weather data for {city} from Weather API")
    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}"
    response = requests.get(url)

    if response.status_code != 200:
        return {"error": "Failed to fetch weather data"}
    
    data = response.json()
    
    # Prepare data for MongoDB
    weather_record = {
        "city": data["location"]["name"],
        "temperature_celsius": data["current"]["temp_c"],
        "temperature_fahrenheit": data["current"]["temp_f"],
        "condition": data["current"]["condition"]["text"],
        "humidity": data["current"]["humidity"],
        "wind_kph": data["current"]["wind_kph"],
        "timestamp": datetime.utcnow()
    }

    # Store in MongoDB (if exists, replace old data)
    collection.replace_one({"city": city}, weather_record, upsert=True)

    # Invalidate Redis cache for updated city data
    redis_client.delete(city)

    # Store in Redis cache for 5 minutes
    redis_client.setex(city, CACHE_EXPIRY, json.dumps(weather_record))

    return weather_record

@app.get("/weather/history/")
def get_weather_history():
    """Retrieve stored weather data"""
    remove_old_mongo_data()  # Clean expired data before returning history
    history = [serialize_doc(doc) for doc in collection.find()]
    return {"history": history}
