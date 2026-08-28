"""
Agri Gram AI - Core AI logic module
Rule-based smart agriculture engine (offline, no API needed).
Author: Abinaya K
"""

from PIL import Image
import statistics

# ============================================================
#  1. SOIL TYPE DETECTION (from photo color analysis)
# ============================================================
# Simple, explainable approach: analyze average color of the soil
# photo and map it to a soil type. Real ML can replace this later.

SOIL_TYPES = {
    "black":  {"name": "Black Soil (Karisal)",  "ph": "7.0-8.5",
               "crops": ["Cotton", "Sugarcane", "Wheat", "Jowar", "Groundnut"]},
    "red":    {"name": "Red Soil (Semmann)",    "ph": "6.0-7.0",
               "crops": ["Groundnut", "Millets", "Pulses", "Tobacco", "Potato"]},
    "brown":  {"name": "Loamy/Brown Soil",      "ph": "6.0-7.5",
               "crops": ["Rice", "Wheat", "Vegetables", "Sugarcane", "Maize"]},
    "yellow": {"name": "Sandy/Yellow Soil",     "ph": "5.5-6.5",
               "crops": ["Coconut", "Cashew", "Groundnut", "Watermelon"]},
    "gray":   {"name": "Alluvial Soil (Vண்டல்)", "ph": "6.5-7.5",
               "crops": ["Rice", "Wheat", "Sugarcane", "Maize", "Pulses"]},
}


def detect_soil_type(image_path):
    """Analyze average RGB of soil photo -> classify soil type."""
    img = Image.open(image_path).convert("RGB")
    img = img.resize((100, 100))
    pixels = list(img.getdata())
    r = statistics.mean(p[0] for p in pixels)
    g = statistics.mean(p[1] for p in pixels)
    b = statistics.mean(p[2] for p in pixels)

    # Simple color->soil rules
    if r < 90 and g < 90 and b < 90:
        soil = "black"
    elif r > 120 and g < 100 and b < 90:
        soil = "red"
    elif r > 150 and g > 130 and b < 110:
        soil = "yellow"
    elif abs(r - g) < 25 and abs(g - b) < 25 and r > 100:
        soil = "gray"
    else:
        soil = "brown"

    result = SOIL_TYPES[soil].copy()
    result["detected_rgb"] = {"r": round(r), "g": round(g), "b": round(b)}
    result["soil_key"] = soil
    return result


# ============================================================
#  2. CROP RECOMMENDATION (soil + season)
# ============================================================
SEASONS = {
    "kharif":  {"months": "June - October",   "note": "Monsoon crops"},
    "rabi":    {"months": "October - March",  "note": "Winter crops"},
    "zaid":    {"months": "March - June",     "note": "Summer crops"},
}

CROP_DB = {
    "Rice":      {"water": 1200, "duration": 120, "season": "kharif",
                  "method": "Transplanting in puddled field, keep 5cm standing water"},
    "Wheat":     {"water": 450,  "duration": 140, "season": "rabi",
                  "method": "Line sowing, 4-6 irrigations at critical stages"},
    "Cotton":    {"water": 700,  "duration": 180, "season": "kharif",
                  "method": "Ridge planting, drip irrigation recommended"},
    "Sugarcane": {"water": 1800, "duration": 360, "season": "kharif",
                  "method": "Furrow planting of setts, heavy irrigation"},
    "Groundnut": {"water": 500,  "duration": 110, "season": "kharif",
                  "method": "Sow on raised beds, light frequent irrigation"},
    "Maize":     {"water": 600,  "duration": 100, "season": "kharif",
                  "method": "Dibbling seeds, irrigate every 7-10 days"},
    "Millets":   {"water": 350,  "duration": 90,  "season": "kharif",
                  "method": "Broadcasting or line sowing, drought tolerant"},
    "Pulses":    {"water": 400,  "duration": 100, "season": "rabi",
                  "method": "Line sowing, minimal irrigation needed"},
    "Vegetables":{"water": 550,  "duration": 70,  "season": "zaid",
                  "method": "Raised beds, drip irrigation, mulching"},
    "Coconut":   {"water": 900,  "duration": 365, "season": "kharif",
                  "method": "Pit planting, basin irrigation"},
}


def recommend_crops(soil_key, season="kharif"):
    """Return best crops for the given soil + season with details."""
    soil = SOIL_TYPES.get(soil_key, SOIL_TYPES["brown"])
    recommendations = []
    for crop in soil["crops"]:
        info = CROP_DB.get(crop)
        if info and info["season"] == season:
            recommendations.append({
                "crop": crop,
                "water_mm": info["water"],
                "duration_days": info["duration"],
                "method": info["method"],
                "season": season
            })
    # If none match the season, still return soil's crops with info
    if not recommendations:
        for crop in soil["crops"]:
            info = CROP_DB.get(crop, {"water": 500, "duration": 100,
                                      "method": "General cultivation practice"})
            recommendations.append({
                "crop": crop,
                "water_mm": info.get("water", 500),
                "duration_days": info.get("duration", 100),
                "method": info.get("method", "General cultivation practice"),
                "season": info.get("season", season)
            })
    return recommendations


# ============================================================
#  3. SMART WATER CALCULATOR
# ============================================================
def water_requirement(crop, area_acres=1, temperature=30, rainfall_mm=0):
    """
    Estimate water needed (liters) for a crop.
    Adjusts for temperature (hotter = more) and rainfall (offsets need).
    """
    info = CROP_DB.get(crop, {"water": 500, "duration": 100})
    base_mm = info["water"]  # total mm over crop cycle

    # Temperature factor: +3% per degree above 30C
    temp_factor = 1 + max(0, (temperature - 30)) * 0.03
    # Rainfall offsets requirement
    effective_mm = max(0, base_mm - rainfall_mm) * temp_factor

    # 1 mm over 1 acre (4046.86 m2) = 4046.86 liters
    liters_total = effective_mm * 4046.86 * area_acres
    liters_per_day = liters_total / info.get("duration", 100)

    return {
        "crop": crop,
        "total_water_liters": round(liters_total),
        "per_day_liters": round(liters_per_day),
        "duration_days": info.get("duration", 100),
        "area_acres": area_acres,
        "note": f"Adjusted for {temperature}°C temp and {rainfall_mm}mm rainfall"
    }


# ============================================================
#  4. CROP CALENDAR / TIMELINE
# ============================================================
def crop_calendar(crop):
    """Generate a simple planting-to-harvest timeline."""
    info = CROP_DB.get(crop, {"duration": 100, "season": "kharif"})
    duration = info["duration"]
    season = info.get("season", "kharif")
    stages = [
        {"stage": "Land Preparation", "day": 0,
         "task": "Plough field, add manure/compost"},
        {"stage": "Sowing/Planting", "day": 5,
         "task": "Sow seeds / transplant seedlings"},
        {"stage": "Germination", "day": int(duration * 0.15),
         "task": "Ensure moisture, protect from pests"},
        {"stage": "Vegetative Growth", "day": int(duration * 0.4),
         "task": "Apply fertilizer, weed control, irrigate"},
        {"stage": "Flowering", "day": int(duration * 0.65),
         "task": "Critical irrigation, monitor for disease"},
        {"stage": "Maturity", "day": int(duration * 0.9),
         "task": "Reduce water, prepare for harvest"},
        {"stage": "Harvest", "day": duration,
         "task": "Harvest at right moisture, dry & store"},
    ]
    return {"crop": crop, "season": SEASONS[season], "total_days": duration,
            "timeline": stages}


# ============================================================
#  5. PLANT DISEASE DETECTION (leaf photo)
# ============================================================
DISEASES = {
    "healthy": {"name": "Healthy Leaf", "treatment": "No action needed. Continue regular care.",
                "severity": "None"},
    "yellow":  {"name": "Nitrogen Deficiency / Chlorosis",
                "treatment": "Apply urea/nitrogen fertilizer. Check drainage.",
                "severity": "Medium"},
    "brown":   {"name": "Fungal Blight (Leaf Spot)",
                "treatment": "Spray Mancozeb/Copper fungicide. Remove infected leaves.",
                "severity": "High"},
    "dark":    {"name": "Bacterial Infection",
                "treatment": "Apply Streptocycline. Avoid overhead irrigation.",
                "severity": "High"},
}


def detect_disease(image_path):
    """Analyze leaf color to estimate plant health / disease."""
    img = Image.open(image_path).convert("RGB")
    img = img.resize((100, 100))
    pixels = list(img.getdata())
    r = statistics.mean(p[0] for p in pixels)
    g = statistics.mean(p[1] for p in pixels)
    b = statistics.mean(p[2] for p in pixels)

    # Healthy leaf = green dominant
    if g > r and g > b and g > 90:
        key = "healthy"
    elif r > 140 and g > 130 and b < 100:
        key = "yellow"
    elif r > 90 and g < 90 and b < 80:
        key = "brown"
    else:
        key = "dark"

    result = DISEASES[key].copy()
    result["detected_rgb"] = {"r": round(r), "g": round(g), "b": round(b)}
    result["disease_key"] = key
    return result


# ============================================================
#  6. TAMIL AI CHAT ASSISTANT (rule-based Q&A)
# ============================================================
CHAT_KB = [
    (["water", "தண்ணீர்", "thanni", "neer"],
     "பயிருக்கு காலை அல்லது மாலை நேரத்தில் தண்ணீர் பாய்ச்சவும். Drip irrigation சிறந்தது. "
     "(Water crops in morning/evening. Drip irrigation is best.)"),
    (["fertilizer", "உரம்", "uram", "manure"],
     "இயற்கை உரம் (compost, farmyard manure) சிறந்தது. NPK உரத்தை பயிர் தேவைக்கேற்ப பயன்படுத்தவும். "
     "(Organic compost is best. Use NPK fertilizer as per crop need.)"),
    (["pest", "பூச்சி", "poochi", "disease", "நோய்"],
     "வேப்பெண்ணெய் (neem oil) தெளிப்பு இயற்கை பூச்சிக்கொல்லி. நோய் இருந்தால் இலையை பறித்து அழிக்கவும். "
     "(Neem oil spray is a natural pesticide. Remove diseased leaves.)"),
    (["rice", "நெல்", "nel", "paddy"],
     "நெல் kharif பருவத்தில் (ஜூன்-அக்டோபர்) நடவு செய்யவும். 5cm தண்ணீர் நிற்க வேண்டும். "
     "(Plant rice in kharif season, keep 5cm standing water.)"),
    (["cotton", "பருத்தி", "paruthi"],
     "பருத்தி கருப்பு மண்ணில் (black soil) சிறப்பாக வளரும். Drip irrigation பயன்படுத்தவும். "
     "(Cotton grows best in black soil. Use drip irrigation.)"),
    (["season", "பருவம்", "paruvam", "time", "when"],
     "Kharif: ஜூன்-அக்டோபர் (மழைக்காலம்), Rabi: அக்டோபர்-மார்ச் (குளிர்), Zaid: மார்ச்-ஜூன் (கோடை). "),
    (["hello", "hi", "வணக்கம்", "vanakkam"],
     "வணக்கம்! 🌾 நான் Agri Gram AI. உங்கள் விவசாய கேள்விகளை கேளுங்கள். "
     "(Hello! I'm Agri Gram AI. Ask me your farming questions.)"),
]


def chat_response(message):
    """Simple keyword-matching Tamil/English farming assistant."""
    msg = message.lower()
    for keywords, answer in CHAT_KB:
        if any(k.lower() in msg for k in keywords):
            return answer
    return ("மன்னிக்கவும், எனக்கு புரியவில்லை. தண்ணீர், உரம், பூச்சி, பருவம், "
            "நெல், பருத்தி பற்றி கேளுங்கள். (Sorry, I didn't understand. Ask about "
            "water, fertilizer, pests, season, rice, or cotton.)")
