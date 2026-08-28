"""
Agri Gram AI - Supabase Online Database Module
Connects to Supabase PostgreSQL for permanent online storage.
Author: Abinaya K
"""

import requests
from datetime import datetime

# Supabase Configuration
SUPABASE_URL = "https://ivhkkqmbidifnqpobslo.supabase.co"
SUPABASE_KEY = "sb_publishable_D069g9-DiJXGqm5Q6Y7VgQ_292tnx7W"

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": "Bearer " + SUPABASE_KEY,
    "Content-Type": "application/json",
    "Prefer": "return=representation"
}


def _get(table, params=""):
    """GET request to Supabase REST API"""
    url = f"{SUPABASE_URL}/rest/v1/{table}?{params}"
    res = requests.get(url, headers=HEADERS)
    return res.json() if res.status_code == 200 else []


def _post(table, data):
    """POST (INSERT) to Supabase REST API"""
    url = f"{SUPABASE_URL}/rest/v1/{table}"
    res = requests.post(url, headers=HEADERS, json=data)
    return res.json() if res.status_code in [200, 201] else {"error": res.text}


# ========== USER FUNCTIONS ==========

def login_user(username, password):
    """Validate user login from Supabase"""
    url = f"{SUPABASE_URL}/rest/v1/users?username=eq.{username}&password=eq.{password}"
    res = requests.get(url, headers=HEADERS)
    users = res.json() if res.status_code == 200 else []
    if users and len(users) > 0:
        user = users[0]
        return {"success": True, "user_id": user["id"], "username": user["username"],
                "name": user["name"], "role": user.get("role", "user"), "location": user.get("location", "")}
    return {"success": False, "error": "Invalid username or password"}


def register_user(username, password, name, location="Coimbatore"):
    """Register new user in Supabase"""
    # Check if username exists
    existing = _get("users", f"username=eq.{username}")
    if existing and len(existing) > 0:
        return {"success": False, "error": "Username already exists"}
    
    data = {
        "username": username,
        "password": password,
        "name": name,
        "role": "user",
        "location": location
    }
    result = _post("users", data)
    if "error" in result:
        return {"success": False, "error": str(result["error"])}
    return {"success": True, "message": "Registration successful"}


# ========== IoT DATA FUNCTIONS ==========

def save_iot_data(temperature, humidity, soil_moisture, device_id="ESP32_01"):
    """Save IoT sensor reading to Supabase"""
    alert = ""
    if soil_moisture < 30:
        alert = "Low soil moisture! Irrigation needed."
    if temperature > 40:
        alert += " High temperature alert!"
    if humidity > 90:
        alert += " High humidity - disease risk!"
    
    data = {
        "device_id": device_id,
        "temperature": temperature,
        "humidity": humidity,
        "soil_moisture": soil_moisture,
        "alert": alert.strip() if alert else "OK"
    }
    _post("iot_data", data)
    return {"saved": True, "alert": alert.strip() if alert else "OK"}


def get_iot_history(limit=50):
    """Get recent IoT readings from Supabase"""
    return _get("iot_data", f"order=recorded_at.desc&limit={limit}")


def get_iot_latest():
    """Get latest IoT reading"""
    data = _get("iot_data", "order=recorded_at.desc&limit=1")
    return data[0] if data else None


# ========== CROP HISTORY FUNCTIONS ==========

def save_crop_history(user_id, crop_name, season, area, risk_score, profit):
    """Save crop analysis to Supabase"""
    data = {
        "user_id": user_id,
        "crop_name": crop_name,
        "season": season,
        "area_acres": area,
        "risk_score": risk_score,
        "profit_estimate": profit,
        "planted_date": datetime.now().strftime("%Y-%m-%d")
    }
    _post("crop_history", data)
    return {"saved": True}


def get_crop_history(user_id=None, limit=20):
    """Get crop history from Supabase"""
    if user_id:
        return _get("crop_history", f"user_id=eq.{user_id}&order=created_at.desc&limit={limit}")
    return _get("crop_history", f"order=created_at.desc&limit={limit}")


# ========== SOIL HISTORY FUNCTIONS ==========

def save_soil_analysis(user_id, soil_type, crops, season):
    """Save soil analysis to Supabase"""
    data = {
        "user_id": user_id,
        "soil_type": soil_type,
        "recommended_crops": str(crops),
        "season": season
    }
    _post("soil_history", data)
    return {"saved": True}


# ========== ADMIN FUNCTIONS ==========

def get_all_users():
    """Get all registered users"""
    return _get("users", "order=created_at.desc")


def get_all_activity(limit=100):
    """Get all activity"""
    activity = []
    crops = _get("crop_history", f"order=created_at.desc&limit={limit}")
    for c in crops:
        c['type'] = 'crop_analysis'
        activity.append(c)
    soils = _get("soil_history", f"order=analyzed_at.desc&limit={limit}")
    for s in soils:
        s['type'] = 'soil_analysis'
        activity.append(s)
    iot = _get("iot_data", f"order=recorded_at.desc&limit={limit}")
    for i in iot:
        i['type'] = 'iot_reading'
        activity.append(i)
    return activity


# ========== DATABASE STATS ==========

def get_db_stats():
    """Get database statistics"""
    users = _get("users", "select=id")
    iot = _get("iot_data", "select=id")
    crops = _get("crop_history", "select=id")
    soils = _get("soil_history", "select=id")
    return {
        "users": len(users) if users else 0,
        "iot_readings": len(iot) if iot else 0,
        "crop_records": len(crops) if crops else 0,
        "soil_analyses": len(soils) if soils else 0,
        "database": "Supabase (PostgreSQL)",
        "url": SUPABASE_URL,
        "status": "connected"
    }


# Test connection on import
def test_connection():
    """Test if Supabase is reachable"""
    try:
        result = _get("users", "limit=1")
        if isinstance(result, list):
            print(f"  ✅ Supabase connected! URL: {SUPABASE_URL}")
            return True
        else:
            print(f"  ⚠️ Supabase response: {result}")
            return False
    except Exception as e:
        print(f"  ❌ Supabase connection failed: {e}")
        return False

test_connection()
