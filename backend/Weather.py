"""
Weather Fetcher using OpenWeatherMap API.

Fetches current weather data for a specified city using the OpenWeatherMap API.
Loads configuration from environment variables and includes error handling.
"""

import os
import requests # type: ignore
from dotenv import load_dotenv # type: ignore

def get_env_variable(variable_name: str) -> str:
    """
    Retrieve the value of an environment variable.
    Raises an EnvironmentError if the variable is not set.
    """
    value = os.getenv(variable_name)
    if not value:
        raise EnvironmentError(f"Environment variable '{variable_name}' is not set.")
    return value

def get_current_weather(city: str, units: str = "metric", lang: str = "en") -> dict:
    """
    Fetch current weather data for a given city from OpenWeatherMap API.
    Returns a dictionary with weather information.
    """
    load_dotenv()
    api_key = get_env_variable("OPENWEATHER_API_KEY")
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": units,
        "lang": lang
    }
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    return response.json()

def get_hourly_forecast(city: str, hours: int = 3, units: str = "metric", lang: str = "en") -> list:
    """
    Fetch hourly weather forecast for a given city from OpenWeatherMap API.
    Returns a list of dictionaries with forecast information for the next 'hours' hours.
    """
    load_dotenv()
    api_key = get_env_variable("OPENWEATHER_API_KEY")
    url = "https://api.openweathermap.org/data/2.5/forecast"
    params = {
        "q": city,
        "appid": api_key,
        "units": units,
        "lang": lang
    }
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()
    # Each forecast is for a 3-hour interval; get the next 'hours' entries
    return data["list"][:hours]

if __name__ == "__main__":
    city = input("Enter city name: ")
    try:
        weather = get_current_weather(city)
        print(f"Weather in {city}: {weather['weather'][0]['description']}, temperature: {weather['main']['temp']}°C")
        forecast = get_hourly_forecast(city)
        for hour in forecast:
            dt_txt = hour["dt_txt"]
            description = hour["weather"][0]["description"]
            temp = hour["main"]["temp"]
            print(f"Forecast for {dt_txt}: {description}, temperature: {temp}°C")
    except Exception as e:
        print(f"Error: {e}")
