"""
Agri Gram AI - Flask API Server
Exposes all AI features as REST endpoints.
Author: Abinaya K
"""

import os
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import agri_ai
import agri_features
import agri_extra2
import climate_risk
import iot_module
import supabase_db as database

# Serve the frontend. Works whether index.html sits next to app.py (flat)
# or in a ../frontend folder (structured layout).
_here = os.path.dirname(os.path.abspath(__file__))
_candidates = [_here, os.path.join(_here, "..", "frontend"), os.path.join(_here, "frontend")]
FRONTEND_DIR = next((d for d in _candidates if os.path.exists(os.path.join(d, "index.html"))), _here)
app = Flask(__name__, static_folder=FRONTEND_DIR, static_url_path="")
CORS(app)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.route("/api", methods=["GET"])
def home():
    return jsonify({"app": "Agri Gram AI", "status": "running",
                    "features": ["soil-crop", "weather", "water", "calendar",
                                 "disease", "chat", "profit", "fertilizer",
                                 "rotation", "yield", "alerts", "schemes",
                                 "analytics"]})


# --- 1. Soil photo -> crop recommendation ---
@app.route("/api/soil", methods=["POST"])
def soil():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400
    f = request.files["image"]
    path = os.path.join(UPLOAD_DIR, f.filename)
    f.save(path)

    season = request.form.get("season", "kharif")
    soil_info = agri_ai.detect_soil_type(path)
    crops = agri_ai.recommend_crops(soil_info["soil_key"], season)
    return jsonify({"soil": soil_info, "recommended_crops": crops})


# --- 2. Weather forecast + advice ---
@app.route("/api/weather", methods=["GET"])
def weather():
    """
    Uses free Open-Meteo API (no key needed) if online.
    Falls back to sample data offline.
    """
    city = request.args.get("city", "Coimbatore")
    lat = request.args.get("lat", "11.0168")
    lon = request.args.get("lon", "76.9558")
    try:
        import urllib.request, json
        url = (f"https://api.open-meteo.com/v1/forecast?latitude={lat}"
               f"&longitude={lon}&daily=temperature_2m_max,temperature_2m_min,"
               f"precipitation_sum&timezone=auto&forecast_days=7")
        with urllib.request.urlopen(url, timeout=5) as r:
            data = json.loads(r.read())
        daily = data["daily"]
        forecast = []
        for i in range(len(daily["time"])):
            rain = daily["precipitation_sum"][i]
            advice = ("🌧️ Rain expected - hold irrigation" if rain > 5
                      else "☀️ Dry - irrigate crops")
            forecast.append({
                "date": daily["time"][i],
                "max_temp": daily["temperature_2m_max"][i],
                "min_temp": daily["temperature_2m_min"][i],
                "rainfall_mm": rain,
                "advice": advice
            })
        return jsonify({"city": city, "forecast": forecast, "source": "Open-Meteo"})
    except Exception as e:
        # Offline fallback
        sample = [{"date": f"Day {i+1}", "max_temp": 32, "min_temp": 24,
                   "rainfall_mm": 0, "advice": "☀️ Dry - irrigate crops"}
                  for i in range(7)]
        return jsonify({"city": city, "forecast": sample,
                        "source": "offline-sample", "note": str(e)})


# --- 3. Smart water requirement ---
@app.route("/api/water", methods=["GET"])
def water():
    crop = request.args.get("crop", "Rice")
    area = float(request.args.get("area", 1))
    temp = float(request.args.get("temp", 30))
    rain = float(request.args.get("rain", 0))
    return jsonify(agri_ai.water_requirement(crop, area, temp, rain))


# --- 4. Crop calendar ---
@app.route("/api/calendar", methods=["GET"])
def calendar():
    crop = request.args.get("crop", "Rice")
    return jsonify(agri_ai.crop_calendar(crop))


# --- 5. Disease detection ---
@app.route("/api/disease", methods=["POST"])
def disease():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400
    f = request.files["image"]
    path = os.path.join(UPLOAD_DIR, f.filename)
    f.save(path)
    return jsonify(agri_ai.detect_disease(path))


# --- 6. Tamil AI chat ---
@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    msg = data.get("message", "")
    return jsonify({"reply": agri_ai.chat_response(msg)})


# --- 7. Profit calculator ---
@app.route("/api/profit", methods=["GET"])
def profit():
    crop = request.args.get("crop", "Rice")
    area = float(request.args.get("area", 1))
    price = request.args.get("price")
    price = float(price) if price else None
    return jsonify(agri_features.profit_calculator(crop, area, price))


# --- 8. Fertilizer & pesticide advisor ---
@app.route("/api/fertilizer", methods=["GET"])
def fertilizer():
    crop = request.args.get("crop", "Rice")
    return jsonify(agri_features.fertilizer_advisor(crop))


# --- 9. Crop rotation planner ---
@app.route("/api/rotation", methods=["GET"])
def rotation():
    crop = request.args.get("crop", "Rice")
    return jsonify(agri_features.crop_rotation(crop))


# --- 10. Yield prediction ---
@app.route("/api/yield", methods=["GET"])
def yield_predict():
    crop = request.args.get("crop", "Rice")
    area = float(request.args.get("area", 1))
    rain = float(request.args.get("rain", 800))
    soil = request.args.get("soil", "good")
    return jsonify(agri_features.yield_prediction(crop, area, rain, soil))


# --- 11. Smart weather alerts ---
@app.route("/api/alerts", methods=["GET"])
def alerts():
    temp = float(request.args.get("temp", 30))
    rain = float(request.args.get("rain", 0))
    humidity = float(request.args.get("humidity", 60))
    return jsonify(agri_features.weather_alerts(temp, rain, humidity))


# --- 12. Government schemes ---
@app.route("/api/schemes", methods=["GET"])
def schemes():
    query = request.args.get("q", "")
    return jsonify(agri_features.govt_schemes(query))


# --- 13. Analytics data (for charts) ---
@app.route("/api/analytics", methods=["GET"])
def analytics():
    return jsonify(agri_features.analytics_data())


# --- 14. PDF report generation ---
@app.route("/api/report", methods=["POST"])
def report():
    data = request.get_json() or {}
    pdf = agri_extra2.generate_pdf_report(data)
    return send_file(pdf, mimetype="application/pdf",
                     as_attachment=True, download_name="agri_gram_report.pdf")


# --- 15. SMS / notification (Twilio) ---
@app.route("/api/sms", methods=["POST"])
def sms():
    data = request.get_json() or {}
    to = data.get("to", "")
    crop = data.get("crop", "your crop")
    advice = data.get("advice", "Check weather before irrigating.")
    if not to:
        return jsonify({"error": "Phone number required"}), 400
    message = agri_extra2.build_farm_alert(crop, advice)
    # Prefer Fast2SMS (India). If its key isn't set, it returns a demo
    # response; then we try Twilio as a fallback if that is configured.
    result = agri_extra2.send_sms_fast2sms(to, message)
    if not result.get("sent") and os.environ.get("TWILIO_SID"):
        result = agri_extra2.send_sms(to, message)
    return jsonify(result)


# --- 16. Analytics summary (extra stats) ---
@app.route("/api/analytics_summary", methods=["GET"])
def analytics_summary():
    return jsonify(agri_extra2.analytics_summary())


# --- 17. Climate Risk Score (research feature) ---
@app.route("/api/climate_risk", methods=["GET"])
def climate_risk_route():
    crop = request.args.get("crop", "Rice")
    city = request.args.get("city", "Coimbatore")
    lat = float(request.args.get("lat", 11.0168))
    lon = float(request.args.get("lon", 76.9558))
    return jsonify(climate_risk.climate_risk_score(lat, lon, crop, city))


# --- 18. IoT - receive sensor data from ESP32/Wokwi ---
@app.route("/api/iot/push", methods=["POST"])
def iot_push():
    data = request.get_json() or {}
    result = iot_module.add_reading(data)
    return jsonify(result), 201


# --- 19. IoT - get latest reading ---
@app.route("/api/iot/latest", methods=["GET"])
def iot_latest():
    return jsonify(iot_module.get_latest())


# --- 20. IoT - get history for chart ---
@app.route("/api/iot/history", methods=["GET"])
def iot_history():
    n = int(request.args.get("n", 20))
    return jsonify(iot_module.get_history(n))


# --- 21. IoT - simulate a reading (for demo without hardware) ---
@app.route("/api/iot/simulate", methods=["POST"])
def iot_simulate():
    return jsonify(iot_module.simulate_reading()), 201


# --- DATABASE API ROUTES ---

@app.route("/api/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username", "")
    password = data.get("password", "")
    result = database.login_user(username, password)
    return jsonify(result)


@app.route("/api/register", methods=["POST"])
def register():
    data = request.json
    result = database.register_user(
        data.get("username"), data.get("password"),
        data.get("name", ""), data.get("location", "Coimbatore")
    )
    return jsonify(result)


@app.route("/api/db/iot/save", methods=["POST"])
def db_iot_save():
    data = request.json
    result = database.save_iot_data(
        data.get("temperature", 0), data.get("humidity", 0),
        data.get("soil_moisture", 0), data.get("device_id", "ESP32_01")
    )
    return jsonify(result)


@app.route("/api/db/iot/history", methods=["GET"])
def db_iot_history():
    limit = request.args.get("limit", 50, type=int)
    return jsonify(database.get_iot_history(limit))


@app.route("/api/db/crop/save", methods=["POST"])
def db_crop_save():
    data = request.json
    result = database.save_crop_history(
        data.get("user_id", 1), data.get("crop"), data.get("season"),
        data.get("area", 1), data.get("risk_score", 0), data.get("profit", 0)
    )
    return jsonify(result)


@app.route("/api/db/stats", methods=["GET"])
def db_stats():
    return jsonify(database.get_db_stats())


# --- ADMIN ROUTES (only admin can access) ---

@app.route("/api/admin/users", methods=["GET"])
def admin_users():
    """Get all users — admin only"""
    return jsonify(database.get_all_users())


@app.route("/api/admin/activity", methods=["GET"])
def admin_activity():
    """Get all user activity — admin only"""
    limit = request.args.get("limit", 100, type=int)
    return jsonify(database.get_all_activity(limit))


# --- Serve the frontend (index.html) at the root URL ---
@app.route("/")
def serve_frontend():
    return app.send_static_file("index.html")


@app.route("/dashboard.html")
def serve_dashboard():
    return app.send_static_file("dashboard.html")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"🌾 Agri Gram AI running on port {port}")
    app.run(host="0.0.0.0", port=port)
