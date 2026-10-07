"""
Agri Gram AI - Smart Database Router
--------------------------------------
Tries Supabase (online PostgreSQL) first; automatically falls back to
SQLite (local) if Supabase is paused / unreachable.

This prevents the "Server not running!" error that happens when the free
Supabase project goes to sleep after inactivity.

Author: Abinaya K
"""

import database as local_db   # SQLite - always available locally

# --- Try to load Supabase and check if it is actually reachable ---
online_db = None
SUPABASE_OK = False
try:
    import supabase_db as _sup
    online_db = _sup
    SUPABASE_OK = bool(_sup.test_connection())
except Exception as e:
    print(f"  Supabase unavailable at startup -> using local SQLite. ({e})")

if SUPABASE_OK:
    print("  Database mode: ONLINE (Supabase) with SQLite fallback")
else:
    print("  Database mode: LOCAL (SQLite) - Supabase is paused/unreachable")


def _online():
    return SUPABASE_OK and online_db is not None


# ========== USER FUNCTIONS ==========

def login_user(username, password):
    if _online():
        try:
            res = online_db.login_user(username, password)
            if res.get("success"):
                return res
        except Exception as e:
            print(f"  Supabase login error, falling back to SQLite: {e}")
    # Fallback (also serves the seeded demo users: admin / farmer / abinaya ...)
    return local_db.login_user(username, password)


def register_user(username, password, name, location="Coimbatore"):
    if _online():
        try:
            res = online_db.register_user(username, password, name, location)
            if res.get("success"):
                # mirror into local DB so offline login also works
                try:
                    local_db.register_user(username, password, name, location)
                except Exception:
                    pass
            return res
        except Exception as e:
            print(f"  Supabase register error, falling back to SQLite: {e}")
    return local_db.register_user(username, password, name, location)


# ========== IoT DATA FUNCTIONS ==========

def save_iot_data(temperature, humidity, soil_moisture, device_id="ESP32_01"):
    if _online():
        try:
            return online_db.save_iot_data(temperature, humidity, soil_moisture, device_id)
        except Exception as e:
            print(f"  Supabase save_iot_data error, falling back: {e}")
    return local_db.save_iot_data(temperature, humidity, soil_moisture, device_id)


def get_iot_history(limit=50):
    if _online():
        try:
            return online_db.get_iot_history(limit)
        except Exception as e:
            print(f"  Supabase get_iot_history error, falling back: {e}")
    return local_db.get_iot_history(limit)


def get_iot_latest():
    if _online():
        try:
            return online_db.get_iot_latest()
        except Exception as e:
            print(f"  Supabase get_iot_latest error, falling back: {e}")
    return local_db.get_iot_latest()


# ========== CROP HISTORY FUNCTIONS ==========

def save_crop_history(user_id, crop_name, season, area, risk_score, profit):
    if _online():
        try:
            return online_db.save_crop_history(user_id, crop_name, season, area, risk_score, profit)
        except Exception as e:
            print(f"  Supabase save_crop_history error, falling back: {e}")
    return local_db.save_crop_history(user_id, crop_name, season, area, risk_score, profit)


def get_crop_history(user_id=None, limit=20):
    if _online():
        try:
            return online_db.get_crop_history(user_id, limit)
        except Exception as e:
            print(f"  Supabase get_crop_history error, falling back: {e}")
    return local_db.get_crop_history(user_id, limit)


# ========== SOIL HISTORY FUNCTIONS ==========

def save_soil_analysis(user_id, soil_type, crops, season):
    if _online():
        try:
            return online_db.save_soil_analysis(user_id, soil_type, crops, season)
        except Exception as e:
            print(f"  Supabase save_soil_analysis error, falling back: {e}")
    return local_db.save_soil_analysis(user_id, soil_type, crops, season)


# ========== DATABASE STATS ==========

def get_db_stats():
    if _online():
        try:
            return online_db.get_db_stats()
        except Exception as e:
            print(f"  Supabase get_db_stats error, falling back: {e}")
    return local_db.get_db_stats()


# ========== ADMIN FUNCTIONS ==========

def get_all_users():
    if _online():
        try:
            return online_db.get_all_users()
        except Exception as e:
            print(f"  Supabase get_all_users error, falling back: {e}")
    return local_db.get_all_users()


def get_all_activity(limit=100):
    if _online():
        try:
            return online_db.get_all_activity(limit)
        except Exception as e:
            print(f"  Supabase get_all_activity error, falling back: {e}")
    return local_db.get_all_activity(limit)
