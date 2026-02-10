import random
import datetime
import statistics
from config import EXECUTION_INTERVAL_SEC, VOLTAGE_ESP32, BATTERY_CAPACITY


# ================= BATTERY =================
class Battery:
    def __init__(self):
        self.capacity = BATTERY_CAPACITY
        self.energy = random.uniform(0.4, 0.9) * self.capacity

    def consume(self, power):
        self.energy = max(0, self.energy - power)

    def charge(self, power):
        self.energy = min(self.capacity, self.energy + power)

    def percent(self):
        return (self.energy / self.capacity) * 100


# ================= NODE =================
class SensorNode:
    def __init__(self, lat, lon):
        self.id = random.randint(1000, 9999)
        self.latitude = lat
        self.longitude = lon
        self.battery = Battery()
        self.state = "NORMAL"
        self.data = {}
        self.anomaly = False

        self.history = {
            "time": [],
            "temperature": [],
            "humidity": [],
            "battery": []
        }

    def detect_anomaly(self):
        if len(self.history["temperature"]) < 5:
            return False

        temp_std = statistics.stdev(self.history["temperature"])
        hum_std = statistics.stdev(self.history["humidity"])

        if temp_std > 3 or hum_std > 10:
            return True

        return False

    def update(self, weather):
        temp = weather["temperature"] + random.uniform(-1.5, 1.5)
        hum = weather["humidity"] + random.uniform(-5, 5)
        clouds = weather["clouds"]

        esp_power = VOLTAGE_ESP32 * random.uniform(0.15, 0.35)
        sensor_power = 5 * random.uniform(0.002, 0.005)

        self.battery.consume(
            (esp_power + sensor_power) * EXECUTION_INTERVAL_SEC / 3600
        )

        now_hour = datetime.datetime.now().hour
        sunrise = datetime.datetime.fromtimestamp(weather["sunrise"]).hour
        sunset = datetime.datetime.fromtimestamp(weather["sunset"]).hour

        solar = 0
        if sunrise <= now_hour <= sunset:
            solar = random.uniform(300, 700)
            solar *= (1 - clouds / 100)
            solar *= random.uniform(0.08, 0.2)

        self.battery.charge(solar * EXECUTION_INTERVAL_SEC / 3600)

        percent = self.battery.percent()

        if percent < 20:
            self.state = "CRITICAL"
        elif percent < 50:
            self.state = "WARNING"
        else:
            self.state = "NORMAL"

        self.data = {
            "temperature": round(temp, 2),
            "humidity": round(hum, 2),
            "battery": round(percent, 2),
            "solar": round(solar, 2)
        }

        self.history["time"].append(datetime.datetime.now().strftime("%H:%M:%S"))
        self.history["temperature"].append(temp)
        self.history["humidity"].append(hum)
        self.history["battery"].append(percent)

        self.anomaly = self.detect_anomaly()
