# 🌤️ FastAPI Weather Service

A production-ready weather data service built with **FastAPI**, powered by:

- 🚀 **MongoDB** for persistent historical storage  
- ⚡ **Redis** for blazing-fast caching  
- 🌐 **WeatherAPI** for live weather data  
- 🛠️ **Jenkins** for CI/CD and Docker image deployment

---

## 📦 Features

- ✅ **Live Weather Fetching** via WeatherAPI
- ⚡ **5-Minute Redis Caching** for repeated queries
- 🧠 **MongoDB History** with auto-cleanup after 10 minutes
- 🔁 **Smart Eviction** from MongoDB and Redis
- 📄 **Historical Endpoint** to retrieve recent weather logs
- 🐳 **Dockerized Build & Jenkins Pipeline** for CI/CD automation

---

## 🧪 Endpoints

### `GET /weather/?city=London`
Fetches current weather for a city.
- ✅ Checks **Redis cache** first
- ✅ Falls back to **MongoDB**
- ✅ Calls **WeatherAPI** only if needed
- ✅ Saves result to both MongoDB and Redis

### `GET /weather/history/`
Retrieves stored weather data from MongoDB.
- 🧹 Auto-cleans entries older than **10 minutes**
- ✅ Useful for debugging and monitoring usage

---

## 🔧 Environment Setup

Create a `.env` file in the root directory:

```env
WEATHER_API_KEY=your_weatherapi_key
MONGO_URI=mongodb://localhost:27017
REDIS_HOST=localhost
REDIS_PORT=6379
