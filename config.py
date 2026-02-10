import os
from dotenv import load_dotenv

load_dotenv()

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

if not OPENWEATHER_API_KEY:
    raise RuntimeError("OPENWEATHER_API_KEY bulunamadı")

EXECUTION_INTERVAL_SEC = 60
VOLTAGE_ESP32 = 3.3
BATTERY_CAPACITY = 5000
