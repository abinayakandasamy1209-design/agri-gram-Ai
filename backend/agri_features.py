"""
Agri Gram AI - Extra Features Module
New advanced features: profit, fertilizer, crop rotation, yield,
weather alerts, govt schemes, analytics, voice-ready responses.
Author: Abinaya K
"""

# ============================================================
#  Shared crop data (economics + agronomy)
# ============================================================
# All values are approximate, India-focused, for educational demo.
CROP_ECONOMICS = {
    #            cost/acre  price/kg  yield kg/acre  fertilizer         pesticide
    "Rice":      {"cost": 25000, "price": 22, "yield": 2500,
                  "fertilizer": "Urea + DAP + Potash (120:60:40 kg/acre)",
                  "pesticide": "Cartap Hydrochloride for stem borer",
                  "npk": "N:120 P:60 K:40"},
    "Wheat":     {"cost": 20000, "price": 24, "yield": 1800,
                  "fertilizer": "Urea + DAP (100:50 kg/acre)",
                  "pesticide": "Mancozeb for rust disease",
                  "npk": "N:100 P:50 K:25"},
    "Cotton":    {"cost": 35000, "price": 70, "yield": 800,
                  "fertilizer": "Urea + SSP + MOP (80:40:40 kg/acre)",
                  "pesticide": "Imidacloprid for bollworm",
                  "npk": "N:80 P:40 K:40"},
    "Sugarcane": {"cost": 45000, "price": 3.5, "yield": 35000,
                  "fertilizer": "Urea + DAP + Potash (150:80:60 kg/acre)",
                  "pesticide": "Chlorpyrifos for early shoot borer",
                  "npk": "N:150 P:80 K:60"},
    "Groundnut": {"cost": 22000, "price": 55, "yield": 1000,
                  "fertilizer": "DAP + Gypsum (25:200 kg/acre)",
                  "pesticide": "Neem oil for leaf miner",
                  "npk": "N:20 P:40 K:20"},
    "Maize":     {"cost": 18000, "price": 20, "yield": 3000,
                  "fertilizer": "Urea + DAP + MOP (100:50:40 kg/acre)",
                  "pesticide": "Emamectin for fall armyworm",
                  "npk": "N:100 P:50 K:40"},
    "Millets":   {"cost": 12000, "price": 35, "yield": 1200,
                  "fertilizer": "Urea + SSP (40:20 kg/acre)",
                  "pesticide": "Neem spray for shoot fly",
                  "npk": "N:40 P:20 K:20"},
    "Pulses":    {"cost": 15000, "price": 80, "yield": 700,
                  "fertilizer": "DAP + Rhizobium culture (50 kg/acre)",
                  "pesticide": "Neem oil for pod borer",
                  "npk": "N:20 P:50 K:20"},
    "Vegetables":{"cost": 30000, "price": 25, "yield": 8000,
                  "fertilizer": "FYM + NPK (10 tons + 60:40:40 kg/acre)",
                  "pesticide": "Neem + Spinosad for caterpillars",
                  "npk": "N:60 P:40 K:40"},
    "Coconut":   {"cost": 40000, "price": 15, "yield": 12000,
                  "fertilizer": "Urea + SSP + MOP per palm",
                  "pesticide": "Neem cake for root grub",
                  "npk": "N:50 P:30 K:120"},
}


# ============================================================
#  1. PROFIT CALCULATOR
# ============================================================
def profit_calculator(crop, area_acres=1, market_price=None):
    """Estimate cost, revenue and profit for a crop."""
    info = CROP_ECONOMICS.get(crop, CROP_ECONOMICS["Rice"])
    price = market_price if market_price else info["price"]

    total_cost = info["cost"] * area_acres
    total_yield = info["yield"] * area_acres
    revenue = total_yield * price
    profit = revenue - total_cost
    roi = round((profit / total_cost) * 100, 1) if total_cost else 0

    return {
        "crop": crop,
        "area_acres": area_acres,
        "yield_kg": total_yield,
        "market_price_per_kg": price,
        "total_cost": total_cost,
        "total_revenue": round(revenue),
        "profit": round(profit),
        "roi_percent": roi,
        "verdict": ("Highly profitable! 🟢" if roi > 100 else
                    "Profitable 🟢" if profit > 0 else "Loss - reconsider 🔴")
    }


# ============================================================
#  2. FERTILIZER & PESTICIDE ADVISOR
# ============================================================
def fertilizer_advisor(crop):
    """Recommend fertilizer + pesticide + schedule for a crop."""
    info = CROP_ECONOMICS.get(crop, CROP_ECONOMICS["Rice"])
    return {
        "crop": crop,
        "fertilizer": info["fertilizer"],
        "npk_ratio": info["npk"],
        "pesticide": info["pesticide"],
        "schedule": [
            {"stage": "Basal (at sowing)", "action": "Apply full P & K + 1/3 N (DAP/SSP + Potash)"},
            {"stage": "Vegetative (25-30 days)", "action": "Apply 1/3 Nitrogen (Urea) + weed control"},
            {"stage": "Flowering (50-60 days)", "action": "Apply remaining 1/3 N + micronutrients"},
            {"stage": "As needed", "action": f"Spray pesticide: {info['pesticide']}"},
        ],
        "tip": "🌱 Prefer organic (compost/FYM) + neem-based pesticides for sustainable farming."
    }


# ============================================================
#  3. CROP ROTATION PLANNER
# ============================================================
ROTATION_MAP = {
    "Rice":      ["Pulses", "Groundnut", "Vegetables"],
    "Wheat":     ["Pulses", "Maize", "Groundnut"],
    "Cotton":    ["Pulses", "Wheat", "Groundnut"],
    "Sugarcane": ["Pulses", "Vegetables", "Wheat"],
    "Groundnut": ["Rice", "Maize", "Millets"],
    "Maize":     ["Pulses", "Groundnut", "Vegetables"],
    "Millets":   ["Pulses", "Groundnut", "Vegetables"],
    "Pulses":    ["Rice", "Wheat", "Cotton", "Maize"],
    "Vegetables":["Pulses", "Millets", "Groundnut"],
    "Coconut":   ["Pulses", "Vegetables (intercrop)"],
}


def crop_rotation(current_crop):
    """Suggest next crops to maintain soil health."""
    suggestions = ROTATION_MAP.get(current_crop, ["Pulses", "Groundnut"])
    is_legume = current_crop in ["Pulses", "Groundnut"]
    return {
        "current_crop": current_crop,
        "next_crop_options": suggestions,
        "reason": ("Legumes fix nitrogen in soil - great for rotation!"
                   if is_legume else
                   "Rotate with legumes (Pulses/Groundnut) to restore nitrogen "
                   "and break pest cycles."),
        "benefit": "🌱 Improves soil fertility, reduces pests & diseases, boosts next yield.",
        "avoid": f"Don't grow {current_crop} again immediately - depletes same nutrients."
    }


# ============================================================
#  4. YIELD PREDICTION
# ============================================================
def yield_prediction(crop, area_acres=1, rainfall_mm=800, soil_quality="good"):
    """Predict expected harvest based on conditions."""
    info = CROP_ECONOMICS.get(crop, CROP_ECONOMICS["Rice"])
    base = info["yield"]

    # Rainfall factor (ideal ~800mm)
    if rainfall_mm < 400:
        rain_factor = 0.6
    elif rainfall_mm < 700:
        rain_factor = 0.85
    elif rainfall_mm <= 1200:
        rain_factor = 1.0
    else:
        rain_factor = 0.9  # too much rain

    # Soil quality factor
    soil_factor = {"poor": 0.7, "average": 0.85, "good": 1.0, "excellent": 1.15}.get(
        soil_quality.lower(), 1.0)

    predicted = base * area_acres * rain_factor * soil_factor
    return {
        "crop": crop,
        "area_acres": area_acres,
        "predicted_yield_kg": round(predicted),
        "predicted_yield_tons": round(predicted / 1000, 2),
        "rainfall_mm": rainfall_mm,
        "soil_quality": soil_quality,
        "confidence": f"{round(rain_factor * soil_factor * 100)}% of ideal conditions",
        "note": "Prediction based on rainfall & soil quality vs ideal conditions."
    }


# ============================================================
#  5. SMART WEATHER ALERTS
# ============================================================
def weather_alerts(temperature, rainfall_mm, humidity=60):
    """Generate farming alerts based on weather conditions."""
    alerts = []
    if rainfall_mm > 50:
        alerts.append({"level": "⚠️ High", "msg": "Heavy rain expected! Hold irrigation & delay sowing. Ensure drainage."})
    elif rainfall_mm > 10:
        alerts.append({"level": "🟡 Medium", "msg": "Rain coming - reduce/skip irrigation today."})
    else:
        alerts.append({"level": "🟢 Info", "msg": "Dry weather - irrigate crops as scheduled."})

    if temperature > 38:
        alerts.append({"level": "🔴 High", "msg": "Extreme heat! Irrigate in evening, add mulch to retain moisture."})
    elif temperature < 10:
        alerts.append({"level": "🔵 Cold", "msg": "Cold wave - protect seedlings, avoid irrigation at night (frost risk)."})

    if humidity > 80:
        alerts.append({"level": "🟠 Disease Risk", "msg": "High humidity - fungal disease risk! Spray preventive fungicide."})

    return {
        "temperature": temperature, "rainfall_mm": rainfall_mm, "humidity": humidity,
        "alerts": alerts,
        "summary": f"{len(alerts)} alert(s) for your farm today."
    }


# ============================================================
#  6. GOVERNMENT SCHEMES INFO
# ============================================================
GOVT_SCHEMES = [
    {"name": "PM-KISAN", "benefit": "₹6,000/year direct income support (₹2000 x 3 installments)",
     "eligibility": "All landholding farmer families", "how": "Register at pmkisan.gov.in with Aadhaar & land records"},
    {"name": "PM Fasal Bima Yojana (PMFBY)", "benefit": "Crop insurance against natural calamities",
     "eligibility": "All farmers (loanee & non-loanee)", "how": "Apply via bank/CSC/pmfby.gov.in before season"},
    {"name": "Kisan Credit Card (KCC)", "benefit": "Low-interest crop loans up to ₹3 lakh @ 4%",
     "eligibility": "All farmers, tenant farmers, SHGs", "how": "Apply at any bank with land documents"},
    {"name": "Soil Health Card", "benefit": "Free soil testing + nutrient recommendations",
     "eligibility": "All farmers", "how": "Contact local agriculture office / soilhealth.dac.gov.in"},
    {"name": "PM-KUSUM", "benefit": "Subsidy for solar pumps (up to 60%)",
     "eligibility": "Farmers, cooperatives", "how": "Apply via state nodal agency"},
    {"name": "e-NAM", "benefit": "Online market - sell produce at best price nationwide",
     "eligibility": "All farmers", "how": "Register at enam.gov.in via nearby mandi"},
]


def govt_schemes(query=""):
    """Return government schemes, optionally filtered by keyword."""
    if query:
        q = query.lower()
        filtered = [s for s in GOVT_SCHEMES
                    if q in s["name"].lower() or q in s["benefit"].lower()]
        return {"schemes": filtered or GOVT_SCHEMES, "count": len(filtered or GOVT_SCHEMES)}
    return {"schemes": GOVT_SCHEMES, "count": len(GOVT_SCHEMES)}


# ============================================================
#  7. ANALYTICS DATA (for charts)
# ============================================================
def analytics_data():
    """Provide data for dashboard charts (profit & water comparison)."""
    crops = list(CROP_ECONOMICS.keys())
    profit_chart = []
    for c in crops:
        info = CROP_ECONOMICS[c]
        revenue = info["yield"] * info["price"]
        profit = revenue - info["cost"]
        profit_chart.append({"crop": c, "profit_per_acre": round(profit)})

    # sort by profit
    profit_chart.sort(key=lambda x: x["profit_per_acre"], reverse=True)

    return {
        "profit_comparison": profit_chart,
        "best_crop": profit_chart[0]["crop"],
        "note": "Profit per acre comparison (approximate, educational)."
    }
