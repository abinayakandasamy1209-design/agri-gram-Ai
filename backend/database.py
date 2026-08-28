"""
Agri Gram AI - SQLite Database Module
Handles: User login, IoT sensor data, crop history
Author: Abinaya K
"""

import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "agri_gram.db")


def get_connection():
    """Get SQLite database connection"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Create all tables if not exist"""
    conn = get_connection()
    cursor = conn.cursor()

    # Users table (for login)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            name TEXT,
            role TEXT DEFAULT 'user',
            location TEXT DEFAULT 'Coimbatore',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # IoT sensor data table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS iot_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            device_id TEXT DEFAULT 'ESP32_01',
            temperature REAL,
            humidity REAL,
            soil_moisture REAL,
            alert TEXT,
            recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Crop history table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS crop_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            crop_name TEXT,
            season TEXT,
            area_acres REAL,
            risk_score REAL,
            profit_estimate REAL,
            planted_date TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    # Soil analysis history
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS soil_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            soil_type TEXT,
            recommended_crops TEXT,
            season TEXT,
            analyzed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    # Insert default user (farmer/farmer123)
    cursor.execute("""
        INSERT OR IGNORE INTO users (username, password, name, role, location)
        VALUES ('farmer', 'farmer123', 'Farmer User', 'user', 'Coimbatore')
    """)

    # Insert admin user
    cursor.execute("""
        INSERT OR IGNORE INTO users (username, password, name, role, location)
        VALUES ('admin', 'admin123', 'Admin', 'admin', 'Tamil Nadu')
    """)

    # Insert abinaya user
    cursor.execute("""
        INSERT OR IGNORE INTO users (username, password, name, role, location)
        VALUES ('abinaya', 'abinaya123', 'Abinaya K', 'user', 'Coimbatore')
    """)

    # Insert dhanusha user
    cursor.execute("""
        INSERT OR IGNORE INTO users (username, password, name, role, location)
        VALUES ('dhanusha', 'dhanusha123', 'Dhanusha', 'user', 'Coimbatore')
    """)

    # Insert demo users for testing
    cursor.execute("""
        INSERT OR IGNORE INTO users (username, password, name, role, location)
        VALUES ('ravi', 'ravi123', 'Ravi Kumar', 'user', 'Madurai')
    """)
    cursor.execute("""
        INSERT OR IGNORE INTO users (username, password, name, role, location)
        VALUES ('priya', 'priya123', 'Priya S', 'user', 'Salem')
    """)

    conn.commit()
    conn.close()
    print(f"  Database initialized: {DB_PATH}")


# ========== USER FUNCTIONS ==========

def login_user(username, password):
    """Validate user login"""
    conn = get_connection()
    user = conn.execute(
        "SELECT id, username, name, role, location FROM users WHERE username=? AND password=?",
        (username, password)
    ).fetchone()
    conn.close()
    if user:
        return {"success": True, "user_id": user["id"], "username": user["username"],
                "name": user["name"], "role": user["role"], "location": user["location"]}
    return {"success": False, "error": "Invalid username or password"}


def register_user(username, password, name, location="Coimbatore"):
    """Register new user"""
    conn = get_connection()
    try:
        conn.execute(
            "INSERT INTO users (username, password, name, location) VALUES (?, ?, ?, ?)",
            (username, password, name, location)
        )
        conn.commit()
        conn.close()
        return {"success": True, "message": "Registration successful"}
    except sqlite3.IntegrityError:
        conn.close()
        return {"success": False, "error": "Username already exists"}


# ========== IoT DATA FUNCTIONS ==========

def save_iot_data(temperature, humidity, soil_moisture, device_id="ESP32_01"):
    """Save IoT sensor reading to database"""
    alert = ""
    if soil_moisture < 30:
        alert = "Low soil moisture! Irrigation needed."
    if temperature > 40:
        alert += " High temperature alert!"
    if humidity > 90:
        alert += " High humidity - disease risk!"

    conn = get_connection()
    conn.execute(
        "INSERT INTO iot_data (device_id, temperature, humidity, soil_moisture, alert) VALUES (?, ?, ?, ?, ?)",
        (device_id, temperature, humidity, soil_moisture, alert.strip())
    )
    conn.commit()
    conn.close()
    return {"saved": True, "alert": alert.strip() if alert else "OK"}


def get_iot_history(limit=50):
    """Get recent IoT readings"""
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM iot_data ORDER BY recorded_at DESC LIMIT ?", (limit,)
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_iot_latest():
    """Get latest IoT reading"""
    conn = get_connection()
    row = conn.execute(
        "SELECT * FROM iot_data ORDER BY recorded_at DESC LIMIT 1"
    ).fetchone()
    conn.close()
    return dict(row) if row else None


# ========== CROP HISTORY FUNCTIONS ==========

def save_crop_history(user_id, crop_name, season, area, risk_score, profit):
    """Save crop analysis to history"""
    conn = get_connection()
    conn.execute(
        """INSERT INTO crop_history (user_id, crop_name, season, area_acres, risk_score, profit_estimate, planted_date)
        VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (user_id, crop_name, season, area, risk_score, profit, datetime.now().strftime("%Y-%m-%d"))
    )
    conn.commit()
    conn.close()
    return {"saved": True}


def get_crop_history(user_id=None, limit=20):
    """Get crop history"""
    conn = get_connection()
    if user_id:
        rows = conn.execute(
            "SELECT * FROM crop_history WHERE user_id=? ORDER BY created_at DESC LIMIT ?",
            (user_id, limit)
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT * FROM crop_history ORDER BY created_at DESC LIMIT ?", (limit,)
        ).fetchall()
    conn.close()
    return [dict(row) for row in rows]


# ========== SOIL HISTORY FUNCTIONS ==========

def save_soil_analysis(user_id, soil_type, crops, season):
    """Save soil analysis result"""
    conn = get_connection()
    conn.execute(
        "INSERT INTO soil_history (user_id, soil_type, recommended_crops, season) VALUES (?, ?, ?, ?)",
        (user_id, soil_type, str(crops), season)
    )
    conn.commit()
    conn.close()
    return {"saved": True}


# ========== DATABASE STATS ==========

def get_db_stats():
    """Get database statistics"""
    conn = get_connection()
    stats = {
        "users": conn.execute("SELECT COUNT(*) FROM users").fetchone()[0],
        "iot_readings": conn.execute("SELECT COUNT(*) FROM iot_data").fetchone()[0],
        "crop_records": conn.execute("SELECT COUNT(*) FROM crop_history").fetchone()[0],
        "soil_analyses": conn.execute("SELECT COUNT(*) FROM soil_history").fetchone()[0],
        "db_file": DB_PATH,
        "db_size_kb": round(os.path.getsize(DB_PATH) / 1024, 1) if os.path.exists(DB_PATH) else 0
    }
    conn.close()
    return stats


# ========== ADMIN FUNCTIONS ==========

def get_all_users():
    """Admin: Get all registered users"""
    conn = get_connection()
    rows = conn.execute(
        "SELECT id, username, name, role, location, created_at FROM users ORDER BY created_at DESC"
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_all_activity(limit=100):
    """Admin: Get all user activity (crop + soil + IoT)"""
    conn = get_connection()
    activity = []
    # Crop history with username
    crops = conn.execute("""
        SELECT c.*, u.username, u.name as user_name 
        FROM crop_history c LEFT JOIN users u ON c.user_id = u.id 
        ORDER BY c.created_at DESC LIMIT ?
    """, (limit,)).fetchall()
    for row in crops:
        d = dict(row)
        d['type'] = 'crop_analysis'
        activity.append(d)
    
    # Soil history with username
    soils = conn.execute("""
        SELECT s.*, u.username, u.name as user_name 
        FROM soil_history s LEFT JOIN users u ON s.user_id = u.id 
        ORDER BY s.analyzed_at DESC LIMIT ?
    """, (limit,)).fetchall()
    for row in soils:
        d = dict(row)
        d['type'] = 'soil_analysis'
        activity.append(d)
    
    # IoT readings
    iot = conn.execute(
        "SELECT * FROM iot_data ORDER BY recorded_at DESC LIMIT ?", (limit,)
    ).fetchall()
    for row in iot:
        d = dict(row)
        d['type'] = 'iot_reading'
        activity.append(d)
    
    conn.close()
    # Sort all by time
    activity.sort(key=lambda x: x.get('created_at') or x.get('analyzed_at') or x.get('recorded_at') or '', reverse=True)
    return activity


# Initialize database when module is imported
init_db()
