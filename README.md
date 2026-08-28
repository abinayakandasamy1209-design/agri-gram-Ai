# 🌾 Agri Gram AI — Smart Farming Assistant

An AI-powered web application that helps farmers make smart decisions:
**which crop to grow, how much water to use, when to plant/harvest, weather advice,
plant disease detection, and a Tamil/English farming chatbot** — all in one.

> Software-only mini project · by **Abinaya K** · 3rd Year CSE
> Domain: **AI · Full-stack · Agriculture**

---

## 🎯 Problem Statement

Farmers often don't know:
- ⏰ **When** and **what** crop will yield best in their land
- 🌦️ **How the weather** will behave over the coming days
- 📸 **Which crops** suit their soil (just from a land photo)
- 💧 **How much water** a crop actually needs
- 🐛 **What disease** affects their plant and how to treat it

**Agri Gram AI** solves all of this in a simple, farmer-friendly web app — even in Tamil.

---

## ✨ Features

| # | Feature | What it does |
|---|---------|--------------|
| 📸 | **Soil Photo → Crop** | Upload a soil/land photo → AI detects soil type → suggests best crops with growing method |
| 🌦️ | **Weather Forecast** | 7-day forecast + smart advice ("irrigate" / "hold water, rain coming") |
| 💧 | **Smart Water Calc** | Crop + area + temp + rainfall → exact liters needed per day |
| 📅 | **Crop Calendar** | Full planting-to-harvest timeline with tasks per stage |
| 🐛 | **Disease Detection** | Upload leaf photo → detects health issue → suggests treatment |
| 🗣️ | **Tamil AI Chat** | Ask farming questions in Tamil/English, get instant answers |

---

## 🏗️ Architecture

```
┌──────────────┐   REST API    ┌──────────────┐    uses    ┌──────────────┐
│  Web Frontend│ ◄───────────► │  Flask API   │ ─────────► │  AI Engine   │
│  (HTML/JS)   │   fetch/JSON   │  (app.py)    │            │ (agri_ai.py) │
│  6 feature   │                │  6 endpoints │            │ image + rule │
│  tabs        │                │              │            │  based logic │
└──────────────┘                └──────────────┘            └──────────────┘
                                        │
                                        ▼
                                 Open-Meteo API
                                 (free weather, no key)
```

---

## 🧰 Tech Stack

| Layer     | Technology                          |
|-----------|-------------------------------------|
| Frontend  | HTML, CSS, JavaScript (Fetch API)   |
| Backend   | Python, Flask, Flask-CORS           |
| AI Logic  | Pillow (image analysis) + rule-based engine |
| Weather   | Open-Meteo API (free, no API key)   |

> **Why rule-based AI?** It's offline, explainable, fast, and needs no dataset —
> perfect for a mini project. Easy to upgrade to a trained ML model later.

---

## 📂 Project Structure

```
agri-gram-ai/
├── backend/
│   ├── app.py            # Flask API (6 endpoints)
│   ├── agri_ai.py        # Core AI logic (all features)
│   └── requirements.txt
├── frontend/
│   └── index.html        # Full dashboard (6 feature tabs)
└── README.md
```

---

## 🚀 How to Run

### 1. Start Backend
```bash
cd backend
pip install -r requirements.txt
python app.py
```
API runs at `http://localhost:5000`

### 2. Open Frontend
Open `frontend/index.html` in your browser. Done! 🎉

---

## 🎬 Demo Flow (for viva / presentation)

1. **Soil tab** → upload any soil photo → see detected soil + crop suggestions
2. **Weather tab** → type city → 7-day forecast with advice
3. **Water tab** → pick crop, enter area/temp → get exact water need
4. **Calendar tab** → pick crop → full timeline
5. **Disease tab** → upload leaf photo → health status + treatment
6. **Chat tab** → ask "water eppo vidanum?" → get Tamil answer

---

## 🔮 Future Enhancements
- Real ML model (scikit-learn / TensorFlow) for soil & disease classification
- GPS-based auto location for weather
- Market price integration (profit calculator)
- Voice input in Tamil
- Mobile app version (React Native / Flutter)
- Farmer login + save history

---

## 👨💻 Author
**Abinaya K** — 3rd Year CSE
Domain: AI · Full-stack · Agriculture

⭐ Star this repo if you found it useful!
