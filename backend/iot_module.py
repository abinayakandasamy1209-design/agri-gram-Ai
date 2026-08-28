"""
Agri Gram AI - IoT Module
Receives real-time sensor data from ESP32 (or Wokwi simulation)
and provides live monitoring + auto irrigation alerts.
Author: Abinaya K
"""

from datetime import datetime

# In-memory storage for demo (recent readings)
sensor_history = []
MAX_HISTORY = 50


def add_reading(data):
    """
    Store a sensor reading.
    Expected data: {temperature, humidity, soil_moisture, device}
    """
    reading = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "temperature": float(data.get("temperature", 0)),
        "humidity": float(data.get("humidity", 0)),
        "soil_moisture": float(data.get("soil_moisture", 50)),
        "device": data.get("device", "ESP32-01"),
    }

    # Auto alerts
    alerts = []
    if reading["soil_moisture"] < 30:
        alerts.append("⚠️ Soil moisture LOW! Irrigation needed.")
    if reading["temperature"] > 38:
        alerts.append("🌡️ Extreme heat! Protect crops.")
    if reading["humidity"] > 85:
        alerts.append("🍄 High humidity — fungal disease risk!")
    if reading["soil_moisture"] > 80:
        alerts.append("🌊 Soil too wet — risk of waterlogging!")

    reading["alerts"] = alerts
    reading["irrigation_needed"] = reading["soil_moisture"] < 30

    sensor_history.append(reading)
    if len(sensor_history) > MAX_HISTORY:
        sensor_history.pop(0)

    return reading


def get_latest():
    """Return the most recent reading."""
    if sensor_history:
        return sensor_history[-1]
    return {"message": "No sensor data received yet. Start the ESP32/Wokwi simulation."}


def get_history(n=20):
    """Return the last N readings for charting."""
    return {
        "readings": sensor_history[-n:],
        "count": len(sensor_history),
        "latest": get_latest(),
    }


def simulate_reading():
    """Generate a simulated sensor reading (for testing without ESP32)."""
    import random
    data = {
        "temperature": round(25 + random.uniform(0, 12), 1),
        "humidity": round(50 + random.uniform(0, 35), 1),
        "soil_moisture": round(20 + random.uniform(0, 60), 1),
        "device": "SIMULATOR",
    }
    return add_reading(data)
