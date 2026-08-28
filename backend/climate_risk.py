"""
Agri Gram AI - Climate Risk Score Module
=========================================
A research-oriented feature: given a location's weather forecast,
compute a multi-factor CLIMATE RISK SCORE (0-100) for farming, broken
down into drought, flood, heat-stress and cold-stress sub-risks, plus
a crop-specific vulnerability adjustment.

Novelty (for the paper):
  - Combines 4 climate hazards into a single interpretable risk index.
  - Crop-specific weighting (each crop reacts differently to each hazard).
  - Fully explainable: every sub-score and the reason is returned,
    so the farmer/reviewer sees WHY the risk is high or low.

Author: Abinaya K
"""

import urllib.request
import json


# ------------------------------------------------------------
#  Crop climate sensitivity table (0 = not sensitive, 1 = very sensitive)
#  Rows tuned from general agronomy knowledge (educational demo).
# ------------------------------------------------------------
CROP_SENSITIVITY = {
    #            drought  flood  heat   cold
    "Rice":      {"drought": 0.9, "flood": 0.2, "heat": 0.5, "cold": 0.6},
    "Wheat":     {"drought": 0.6, "flood": 0.7, "heat": 0.8, "cold": 0.3},
    "Cotton":    {"drought": 0.5, "flood": 0.8, "heat": 0.4, "cold": 0.7},
    "Sugarcane": {"drought": 0.8, "flood": 0.4, "heat": 0.3, "cold": 0.6},
    "Groundnut": {"drought": 0.7, "flood": 0.7, "heat": 0.5, "cold": 0.5},
    "Maize":     {"drought": 0.8, "flood": 0.6, "heat": 0.7, "cold": 0.5},
    "Millets":   {"drought": 0.3, "flood": 0.5, "heat": 0.3, "cold": 0.4},
    "Pulses":    {"drought": 0.6, "flood": 0.8, "heat": 0.6, "cold": 0.5},
    "Vegetables":{"drought": 0.7, "flood": 0.7, "heat": 0.8, "cold": 0.7},
    "Coconut":   {"drought": 0.5, "flood": 0.3, "heat": 0.3, "cold": 0.5},
}


def _fetch_forecast(lat, lon):
    """Get 7-day forecast from Open-Meteo (free, no key). Returns dict or None."""
    try:
        url = (f"https://api.open-meteo.com/v1/forecast?latitude={lat}"
               f"&longitude={lon}&daily=temperature_2m_max,temperature_2m_min,"
               f"precipitation_sum&timezone=auto&forecast_days=7")
        with urllib.request.urlopen(url, timeout=6) as r:
            return json.loads(r.read())["daily"]
    except Exception:
        return None


def _hazard_scores(daily):
    """
    Turn raw weather into 4 hazard sub-scores (0-100).
    Higher = more risky. Rules are simple, transparent thresholds.
    """
    tmax = daily["temperature_2m_max"]
    tmin = daily["temperature_2m_min"]
    rain = daily["precipitation_sum"]

    total_rain = sum(rain)
    max_day_rain = max(rain)
    avg_tmax = sum(tmax) / len(tmax)
    min_tmin = min(tmin)

    # --- Drought risk: low total rainfall over the week ---
    if total_rain < 5:
        drought = 90
    elif total_rain < 20:
        drought = 65
    elif total_rain < 50:
        drought = 35
    else:
        drought = 10

    # --- Flood risk: heavy rain on a single day / high weekly total ---
    if max_day_rain > 80 or total_rain > 200:
        flood = 90
    elif max_day_rain > 40 or total_rain > 120:
        flood = 60
    elif max_day_rain > 20:
        flood = 35
    else:
        flood = 10

    # --- Heat stress: high average max temperature ---
    if avg_tmax > 40:
        heat = 90
    elif avg_tmax > 36:
        heat = 65
    elif avg_tmax > 32:
        heat = 35
    else:
        heat = 10

    # --- Cold stress: low minimum temperature ---
    if min_tmin < 5:
        cold = 90
    elif min_tmin < 10:
        cold = 60
    elif min_tmin < 15:
        cold = 30
    else:
        cold = 5

    return {
        "drought": drought, "flood": flood, "heat": heat, "cold": cold,
        "_stats": {
            "total_rain_mm": round(total_rain, 1),
            "max_day_rain_mm": round(max_day_rain, 1),
            "avg_max_temp": round(avg_tmax, 1),
            "min_temp": round(min_tmin, 1),
        }
    }


def _label(score):
    if score >= 70:
        return "🔴 High Risk"
    if score >= 40:
        return "🟠 Moderate Risk"
    if score >= 20:
        return "🟡 Low Risk"
    return "🟢 Safe"


def climate_risk_score(lat=11.0168, lon=76.9558, crop="Rice", city="Coimbatore"):
    """
    Main entry: compute crop-weighted climate risk score for a location.
    Returns a fully explainable breakdown.
    """
    daily = _fetch_forecast(lat, lon)
    source = "Open-Meteo (live)"
    if not daily:
        # Offline fallback sample (so demo always works)
        daily = {
            "temperature_2m_max": [34, 35, 36, 33, 34, 35, 34],
            "temperature_2m_min": [24, 25, 24, 23, 24, 25, 24],
            "precipitation_sum": [0, 0, 2, 0, 1, 0, 0],
        }
        source = "offline-sample"

    hz = _hazard_scores(daily)
    stats = hz.pop("_stats")

    sens = CROP_SENSITIVITY.get(crop, CROP_SENSITIVITY["Rice"])

    # Crop-weighted overall score: each hazard weighted by crop sensitivity.
    # Normalised so the result stays in 0-100.
    weight_sum = sum(sens.values())
    weighted = sum(hz[h] * sens[h] for h in hz) / weight_sum
    overall = round(weighted, 1)

    # Build explainable breakdown
    breakdown = []
    for h in ["drought", "flood", "heat", "cold"]:
        breakdown.append({
            "hazard": h.capitalize(),
            "score": hz[h],
            "label": _label(hz[h]),
            "crop_sensitivity": sens[h],
            "contribution": round(hz[h] * sens[h] / weight_sum, 1),
        })
    breakdown.sort(key=lambda x: x["contribution"], reverse=True)

    top = breakdown[0]
    advice = _advice(top["hazard"], top["score"], crop)

    return {
        "city": city,
        "crop": crop,
        "overall_risk": overall,
        "overall_label": _label(overall),
        "top_hazard": top["hazard"],
        "breakdown": breakdown,
        "weather_stats": stats,
        "advice": advice,
        "source": source,
        "explanation": (
            f"Overall risk {overall}/100 for {crop} near {city}. "
            f"The biggest driver is {top['hazard']} "
            f"(hazard {top['score']}/100 × {crop} sensitivity "
            f"{top['crop_sensitivity']}). Scores combine 7-day forecast "
            f"of rainfall and temperature, weighted by how sensitive this "
            f"crop is to each hazard."
        ),
    }


def _advice(hazard, score, crop):
    """Actionable advice for the dominant hazard."""
    h = hazard.lower()
    if score < 20:
        return f"🟢 Conditions look safe for {crop}. Proceed with normal practices."
    tips = {
        "drought": f"💧 Drought risk for {crop}: arrange drip/mulching, harvest rainwater, "
                   f"prefer drought-tolerant varieties or delay sowing.",
        "flood": f"🌊 Flood risk for {crop}: ensure field drainage, make raised beds, "
                 f"delay sowing until heavy rain passes.",
        "heat": f"🌡️ Heat stress for {crop}: irrigate in early morning/evening, "
                f"use shade nets / mulch, avoid midday spraying.",
        "cold": f"❄️ Cold stress for {crop}: protect seedlings with covers, "
                f"irrigate lightly at night, avoid frost-prone low areas.",
    }
    return tips.get(h, "Monitor weather closely and adapt irrigation.")
