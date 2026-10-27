"""
Agri Gram AI - Smart Database Router
--------------------------------------
Tries Supabase (online PostgreSQL) first; automatically falls back to
SQLite (local) if Supabase is paused / unreachable.

This prevents the "Server not running!" error that happens when the free
Supabase project goes to sleep after inactivity.

Author: Abinaya K
"""

import time
import database as local_db   # SQLite fallback

# --- Supabase Module Loading ---
online_db = None
try:
    import supabase_db as _sup
    online_db = _sup
except Exception:
    online_db = None

_last_check = 0
_cached_online = False

def _online():
    """Dynamically checks if Supabase is reachable (caches for 30s)"""
    global _last_check, _cached_online
    now = time.time()
    if now - _last_check < 30:
        return _cached_online
    _last_check = now
    if online_db is not None:
        try:
            _cached_online = bool(online_db.test_connection())
        except Exception:
            _cached_online = False
    return _cached_online


# Compatibility flag
SUPABASE_OK = _cached_online

def init_db():
    """Initialize local SQLite DB so tables and seeded accounts are guaranteed ready"""
    try:
        local_db.init_db()
    except Exception as e:
        print(f"  [DB] local_db init notice: {e}")

# Initial check
if _online():
    SUPABASE_OK = True
    print("  [DB] Primary Database: ONLINE (Supabase PostgreSQL)")
else:
    SUPABASE_OK = False
    print("  [DB] Primary Database: LOCAL (SQLite fallback) - will auto-reconnect when Supabase wakes")



# ========== USER FUNCTIONS (Supabase Primary) ==========

def login_user(username, password):
    """Try Supabase primary first; fallback to local SQLite"""
    if _online():
        try:
            res = online_db.login_user(username, password)
            if res and res.get("success"):
                return res
        except Exception:
            pass
    # Fallback (also serves seeded demo users: abinaya / farmer / admin)
    return local_db.login_user(username, password)


def register_user(username, password, name, location="Coimbatore"):
    """Try Supabase primary first; mirror to local SQLite"""
    if _online():
        try:
            online_res = online_db.register_user(username, password, name, location)
            # Mirror into local DB so offline access also works
            try:
                local_db.register_user(username, password, name, location)
            except Exception:
                pass
            if online_res and online_res.get("success"):
                return online_res
        except Exception:
            pass
            
    # Local registration if Supabase is offline
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
