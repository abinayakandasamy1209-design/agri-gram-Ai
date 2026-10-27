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

## 🚀 How to Run Locally

### Option 1: One-Click (Windows)
Double-click `run_app.bat` — it starts the server and opens `http://127.0.0.1:5000` automatically!

### Option 2: Terminal
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the application (from project root)
python app.py
```
Open **`http://127.0.0.1:5000`** in your browser.

> **Pre-configured Demo Accounts:**
> - `abinaya` / `abinaya123` (Abinaya K)
> - `farmer` / `farmer123` (Farmer User)
> - `admin` / `admin123` (Admin)

---

## 📱 Progressive Web App (PWA) Features

Agri Gram AI is now a full **Progressive Web App (PWA)** that can be installed on Android smartphones, tablets, and desktops like a native app:
- 📲 **Standalone App Interface**: Launches without browser URL bars, tabs, or navigation controls.
- 🌾 **Custom Branding & Icons**: Tailored golden wheat & emerald green theme with adaptive maskable icons.
- 📡 **Offline Resilience**: Essential app shell and an offline farming advisory page work even when disconnected.
- ⚡ **Fast Mobile Navigation**: Thumb-friendly mobile bottom navigation bar for instant access to Soil, Weather, Water, and Chat tools.
- 🔒 **Secure**: HTTPS-ready with zero exposure of backend keys or secrets.

---

## 🌐 How to Deploy on Render

Deploying Agri Gram AI to Render is automated and requires no manual server configuration:

1. **Push to GitHub**:
   Ensure all changes are pushed to your GitHub repository:
   `https://github.com/abinayakandasamy1209-design/agri-gram-Ai`

2. **Create New Web Service on Render**:
   - Go to [dashboard.render.com](https://dashboard.render.com).
   - Click **New +** → **Web Service**.
   - Select **Build and deploy from a Git repository** and connect your repository: `agri-gram-Ai`.

3. **Configure Service Settings**:
   - **Name**: `agri-gram-ai`
   - **Region**: Closest to you (e.g. Singapore or Frankfurt)
   - **Branch**: `main`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   *(Render will also automatically detect `render.yaml` and `Procfile` if using Blueprint).*

4. **Click "Create Web Service"**:
   Render will install dependencies, configure SSL/HTTPS, and deploy your live URL (e.g. `https://agri-gram-ai.onrender.com`).

---

## 📲 How to Install on Android Mobile (PWA)

Once deployed on Render (or opened over HTTPS/localhost):

### Option A: 1-Tap In-App Install
1. Open your website URL in **Google Chrome** on your Android device.
2. Tap the **"📲 Install Agri Gram App"** banner at the top of the login screen or top navbar.
3. Tap **Install** in the Chrome prompt. The app icon will appear directly on your home screen and app drawer!

### Option B: Chrome Menu ("Add to Home screen")
1. Open your website URL in **Google Chrome** on Android.
2. Tap the **three vertical dots (⋮)** in the top-right corner of Chrome.
3. Tap **"Install app"** or **"Add to Home screen"**.
4. Confirm by tapping **Add** / **Install**.
5. Agri Gram AI will now open in full standalone app mode!

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
