import requests
import os

def get_weather(lat: float, lon: float):
    api_key = os.getenv("OPENWEATHER_API_KEY")

    url = (
        "https://api.openweathermap.org/data/2.5/weather"
        f"?lat={lat}&lon={lon}&units=metric&appid={api_key}"
    )

    r = requests.get(url, timeout=10)
    r.raise_for_status()
    data = r.json()

    return {
        "temperature": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "clouds": data["clouds"]["all"],
        "sunrise": data["sys"]["sunrise"],
        "sunset": data["sys"]["sunset"]
    }
