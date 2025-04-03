import os
import requests
from fastapi import FastAPI, Depends
from dotenv import load_dotenv
from pymongo import MongoClient
from datetime import datetime

# Load environment variables
load_dotenv()

app = FastAPI()

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

@app.get("/weather/")
def get_weather(city: str, api_key: str = Depends(get_weather_api_key)):
    """Fetches and stores the weather data for a given city!!"""
    
    # Check if the city data is already in the DB (cache)
    existing_data = collection.find_one({"city": city})
    if existing_data:
        return {**existing_data, "_id": str(existing_data["_id"])}

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

    # Store in MongoDB
    collection.insert_one(weather_record)

    return weather_record

@app.get("/weather/history/")
def get_weather_history():
    """Retrieve stored weather data"""
    history = list(collection.find({}, {"_id": 0}))  # Exclude MongoDB ObjectID
    return {"history": history}
