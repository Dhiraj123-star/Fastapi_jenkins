import os
import requests
from fastapi import FastAPI, Depends
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI()

# Dependency to get API key securely
def get_weather_api_key():
    api_key = os.getenv("WEATHER_API_KEY")
    if not api_key:
        raise ValueError("Weather API key is missing. Set it in the .env file.")
    return api_key

@app.get("/weather/")
def get_weather(city: str, api_key: str = Depends(get_weather_api_key)):
    """Fetches the weather data for a given city"""
    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}"
    
    response = requests.get(url)
    
    if response.status_code != 200:
        return {"error": "Failed to fetch weather data"}
    
    data = response.json()
    
    return {
        "city": data["location"]["name"],
        "temperature_celsius": data["current"]["temp_c"],
        "temperature_fahrenheit": data["current"]["temp_f"],
        "condition": data["current"]["condition"]["text"],
        "humidity": data["current"]["humidity"],
        "wind_kph": data["current"]["wind_kph"]
    }
