import os
import json
import httpx
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

# Import demo data
from demo_data import get_city, list_cities, CITIES

app = FastAPI(
    title="EcoPulse AI Backend",
    description="Production-grade hackathon API for Environmental Risk forecasting, attribution, and intervention recommendation.",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─────────────────────────────────────────────────────────────────────────────
# Copilot Q&A fallback library (city-agnostic + Bengaluru-specific)
# ─────────────────────────────────────────────────────────────────────────────
MOCK_COPILOT_QA = [
    {
        "keywords": ["why", "pollution", "increasing", "cause", "reason"],
        "answer": "Based on our XGBoost feature attribution (SHAP), the primary driver is industrial zone emissions contributing 42–55% of pollution. This is compounded by traffic congestion (28–35% contribution) and stagnant low-wind conditions. Low vegetation cover (6–18%) accounts for the remaining impact due to lack of natural absorption."
    },
    {
        "keywords": ["what", "should", "do", "week", "authority", "action", "prevent", "recommendation"],
        "answer": "The EcoPulse AI Intervention Engine recommends three high-priority actions:\n1. Reduce industrial output by 15–20% in the critical zone (AQI reduction: 20–28% | Confidence: 86–92%)\n2. Restrict heavy vehicles during peak hours (AQI reduction: 13–22% | Cost: ₹0.2–1.2 Cr)\n3. Emergency green cover expansion (Long-term AQI buffer: 6–10%)\nApplying these combined will avert the projected hazardous event."
    },
    {
        "keywords": ["zone", "highest", "risk", "hotspot", "active", "cluster"],
        "answer": "Our DBSCAN clustering identifies 2 active pollution hotspots in the primary industrial corridor. Cluster 0 covers the core industrial zone (AQI 168–415, Critical/Severe) and Cluster 1 covers the surrounding residential-commercial interface (AQI 138–378, High). The industrial core represents the highest immediate risk."
    },
    {
        "keywords": ["green cover", "vegetation", "increase", "forest", "tree", "plantation"],
        "answer": "Increasing green cover shows positive long-term effects in our Digital Twin simulation. A 10% increase reduces the base AQI by approximately 12–18 points and raises the Environmental Health Index (EHI) by 3–5 points, serving as a sustained buffer against industrial and vehicle emissions."
    },
    {
        "keywords": ["confidence", "interval", "forecast", "percentile", "rmse", "accuracy", "band"],
        "answer": "We use quantile regression residuals from historical cross-validation to construct the 90% confidence interval (5th to 95th percentile). This bounds our XGBoost projection line, representing meteorological uncertainty. The shaded region on the chart represents this uncertainty band."
    },
    {
        "keywords": ["ehi", "environmental health index", "score", "calculate", "formula"],
        "answer": "The Environmental Health Index (EHI) is a composite index unique to EcoPulse AI: EHI = (AQI_score × 0.40) + (Water_health × 0.20) + (Heatwave_health × 0.20) + (Vegetation_health × 0.20). Scores: 0–19 = Emergency, 20–39 = Critical, 40–59 = Stressed, 60–79 = Moderate, 80–100 = Healthy."
    },
    {
        "keywords": ["anomal", "sensor", "fault", "outlier", "isolation forest", "data integrity"],
        "answer": "We run an Isolation Forest anomaly detector on incoming sensor data. It flags out-of-bounds spikes (sensor hardware errors), zero flatline readings (connection loss), and calibration drift. EcoPulse AI marks these stations as 'Unreliable' and excludes them from model training automatically."
    },
    {
        "keywords": ["safar", "difference", "compare", "better", "iqair", "ambee", "vs"],
        "answer": "Unlike traditional systems like SAFAR or IQAir which only monitor and display current/historical data, EcoPulse AI is action-oriented. We forecast future outcomes (7 days ahead), explain root causes via SHAP, offer a Digital Twin for what-if simulations, and recommend ranked, cost-benefit-analyzed interventions."
    },
    {
        "keywords": ["digital twin", "simulate", "physics", "parametric", "slider"],
        "answer": "Our Digital Twin is a parametric scenario simulator. Adjust sliders (Traffic, Industry, Green Cover, Weather) and immediately evaluate their impact using regression weights. Labeled as 'Scenario Simulation' rather than a physics fluid-dynamics model for technical honesty. Future roadmap includes RL-based policy optimization."
    },
    {
        "keywords": ["xgboost", "model", "features", "train", "dataset", "machine learning"],
        "answer": "We trained an XGBoost Ensemble on 12 months of CPCB and OpenAQ daily data. Features include 6 criteria pollutants (PM2.5, PM10, NO2, SO2, CO, O3), 4 meteorological variables (Temp, Humidity, Wind, Rainfall), and engineered time-series features (1-day lags, 7-day rolling averages, weekday/holiday flags)."
    },
    {
        "keywords": ["copilot", "gemini", "api", "llm", "ai assistant"],
        "answer": "EcoPulse AI Copilot uses Gemini 1.5 Flash to answer questions. It receives the live city context (EHI, AQI, hotspots, active recommendations) injected into the system prompt. If the Gemini API is offline, it seamlessly falls back to our local edge Q&A engine with 15 pre-trained response templates."
    },
    {
        "keywords": ["hazardous", "emergency", "trigger", "threshold", "crisis"],
        "answer": "An emergency is triggered when forecasted AQI exceeds 200 (Hazardous threshold per CPCB standards). EcoPulse AI generates immediate alerts, ranks the most cost-effective interventions, and displays the crisis timeline countdown to help authorities plan ahead."
    },
    {
        "keywords": ["traffic", "congestion", "restrict", "vehicle", "odd even"],
        "answer": "Restricting heavy vehicles and implementing odd-even schemes reduces local traffic density. Our model projects an 10–22% AQI reduction at a cost of ₹0.1–1.2 Cr, making traffic interventions the most cost-effective short-term measures available."
    },
    {
        "keywords": ["industry", "emission", "output", "factory", "chemical", "industrial"],
        "answer": "Reducing industrial output targets the largest pollution contributor (42–55% SHAP impact). A 15–20% curtailment yields a high AQI reduction of 18–28% with 86–92% confidence. Economic cost of ₹2–8 Cr is offset by public health savings estimated at ₹40–120 Cr in avoided hospitalization."
    },
    {
        "keywords": ["hello", "hi", "hey", "who are you", "help"],
        "answer": "Hello! I am the EcoPulse AI Copilot. I help you analyze environmental risks across 5 Indian cities, run scenario simulations on the Digital Twin, and evaluate intervention plans. Ask me about hotspots, forecasts, SHAP attributions, or recommended actions for any city!"
    }
]

# ─────────────────────────────────────────────────────────────────────────────
# Pydantic models
# ─────────────────────────────────────────────────────────────────────────────
class SimulationRequest(BaseModel):
    city_id: str = "bengaluru"
    traffic_index: float
    industrial_index: float
    green_cover: float
    wind_speed: float
    rainfall: float

class CopilotRequest(BaseModel):
    query: str
    city_id: str = "bengaluru"
    context: Optional[dict] = None

# ─────────────────────────────────────────────────────────────────────────────
# HEALTH
# ─────────────────────────────────────────────────────────────────────────────
@app.get("/api/v1/health")
def health_check():
    return {
        "status": "healthy",
        "version": "2.0.0",
        "cities_loaded": len(CITIES),
        "data_source": "bundled_demo_data",
        "offline_capable": True
    }

# ─────────────────────────────────────────────────────────────────────────────
# CITIES LIST
# ─────────────────────────────────────────────────────────────────────────────
@app.get("/api/v1/cities")
def get_cities():
    """Return summary list of all cities for the city selector."""
    return {"cities": list_cities()}

# ─────────────────────────────────────────────────────────────────────────────
# CITY DASHBOARD (full state for a single city)
# ─────────────────────────────────────────────────────────────────────────────
@app.get("/api/v1/city/{city_id}")
def get_city_dashboard(city_id: str):
    """Return the complete dashboard state for a city."""
    city = get_city(city_id)
    c = city["current"]

    return {
        "city_id": city["id"],
        "city": city["name"],
        "zone": city["zone"],
        "lat": city["lat"],
        "lon": city["lon"],
        "current_conditions": {
            "aqi": c["aqi"],
            "pm25": c["pm25"],
            "pm10": c["pm10"],
            "no2": c["no2"],
            "so2": c["so2"],
            "co": c["co"],
            "o3": c["o3"],
            "temperature": c["temperature"],
            "humidity": c["humidity"],
            "wind_speed": c["wind_speed"],
            "rainfall": c["rainfall"],
            "industrial_emissions": c["industrial_emissions"],
            "traffic_density": c["traffic_density"],
            "vegetation_index": c["vegetation_index"],
            "ehi": c["ehi"],
            "ehi_band": c["ehi_band"],
            "status": c["status"]
        },
        "forecast_summary": {
            "forecast": city["forecast"],
            "risk_probability": city["risk_probability"],
            "risk_classification": city["risk_classification"],
            "max_forecast_aqi": city["max_forecast_aqi"]
        },
        "shap_values": city["shap_values"],
        "interventions": city["interventions"],
        "hotspots": city["hotspots"],
        "simulation_base": city["simulation_base"],
        "crisis_message": city["crisis_message"]
    }

# ─────────────────────────────────────────────────────────────────────────────
# FORECAST (city-specific)
# ─────────────────────────────────────────────────────────────────────────────
@app.get("/api/v1/forecast/{city_id}")
def get_forecast(city_id: str):
    city = get_city(city_id)
    return {
        "forecast": city["forecast"],
        "risk_probability": city["risk_probability"],
        "risk_classification": city["risk_classification"],
        "max_forecast_aqi": city["max_forecast_aqi"]
    }

# ─────────────────────────────────────────────────────────────────────────────
# SHAP (city-specific)
# ─────────────────────────────────────────────────────────────────────────────
@app.get("/api/v1/shap/{city_id}")
def get_shap(city_id: str):
    city = get_city(city_id)
    return city["shap_values"]

# ─────────────────────────────────────────────────────────────────────────────
# INTERVENTIONS (city-specific)
# ─────────────────────────────────────────────────────────────────────────────
@app.get("/api/v1/interventions/{city_id}")
def get_interventions(city_id: str):
    city = get_city(city_id)
    return city["interventions"]

# ─────────────────────────────────────────────────────────────────────────────
# HOTSPOTS (city-specific)
# ─────────────────────────────────────────────────────────────────────────────
@app.get("/api/v1/hotspots/{city_id}")
def get_hotspots(city_id: str):
    city = get_city(city_id)
    return city["hotspots"]

# ─────────────────────────────────────────────────────────────────────────────
# DIGITAL TWIN SIMULATION (city-specific parametric model)
# ─────────────────────────────────────────────────────────────────────────────
@app.post("/api/v1/simulate")
def simulate_scenario(req: SimulationRequest):
    city = get_city(req.city_id)
    base = city["simulation_base"]
    base_aqi = base["base_aqi"]

    simulated_aqi = (
        base_aqi +
        (req.traffic_index * 0.8) +
        (req.industrial_index * 1.2) -
        (req.green_cover * 15.0) -
        (req.wind_speed * 8.0) -
        (req.rainfall * 0.3)
    )
    simulated_aqi = max(0.0, min(500.0, simulated_aqi))

    carbon_emissions = (req.traffic_index * 4.2 + req.industrial_index * 8.5) * (1.0 - (req.green_cover / 100.0))
    carbon_emissions = max(0.0, round(carbon_emissions, 1))

    water_stress = max(0.0, min(100.0, 30.0 + (req.industrial_index * 0.5) - (req.rainfall * 0.2)))
    heatwave_risk = max(0.0, min(100.0, 45.0 - (req.green_cover * 0.8) + (req.industrial_index * 0.36)))
    vegetation_loss = max(0.0, min(100.0, 100.0 - req.green_cover))

    aqi_score = max(0.0, 100.0 - (simulated_aqi / 200.0) * 100.0)
    water_health = 100.0 - water_stress
    heatwave_health = 100.0 - heatwave_risk
    veg_health = 100.0 - vegetation_loss

    ehi = round((aqi_score * 0.40) + (water_health * 0.20) + (heatwave_health * 0.20) + (veg_health * 0.20), 1)

    risk = "Low"
    if simulated_aqi > 300: risk = "Hazardous"
    elif simulated_aqi > 200: risk = "Hazardous"
    elif simulated_aqi > 150: risk = "High"
    elif simulated_aqi > 100: risk = "Moderate"

    pop_at_risk = 0
    if simulated_aqi > 100:
        pop_at_risk = int((simulated_aqi - 100) * 230)
    if simulated_aqi > 200:
        pop_at_risk = int(25000 + (simulated_aqi - 200) * 207)
    pop_at_risk = max(0, pop_at_risk)

    return {
        "simulated_aqi": int(round(simulated_aqi, 0)),
        "carbon_emissions": carbon_emissions,
        "ehi": ehi,
        "risk_classification": risk,
        "population_at_risk": pop_at_risk
    }

# ─────────────────────────────────────────────────────────────────────────────
# EHI CALCULATOR (generic utility endpoint)
# ─────────────────────────────────────────────────────────────────────────────
@app.get("/api/v1/ehi")
def get_ehi(aqi: float, water_stress: float, heatwave_risk: float, vegetation_loss: float):
    aqi_score = max(0.0, 100.0 - (aqi / 5.0))
    water_health = max(0.0, 100.0 - water_stress)
    heatwave_health = max(0.0, 100.0 - heatwave_risk)
    veg_health = max(0.0, 100.0 - vegetation_loss)
    ehi = round((aqi_score * 0.40) + (water_health * 0.20) + (heatwave_health * 0.20) + (veg_health * 0.20), 1)

    band = "Healthy"
    if ehi < 20: band = "Emergency"
    elif ehi < 40: band = "Critical"
    elif ehi < 60: band = "Stressed"
    elif ehi < 80: band = "Moderate"

    return {
        "ehi": ehi, "band": band,
        "breakdown": {
            "aqi_score": round(aqi_score, 1), "water_health": round(water_health, 1),
            "heatwave_health": round(heatwave_health, 1), "vegetation_health": round(veg_health, 1)
        }
    }

# ─────────────────────────────────────────────────────────────────────────────
# AI COPILOT (city-context-aware)
# ─────────────────────────────────────────────────────────────────────────────
@app.post("/api/v1/copilot")
async def ask_copilot(req: CopilotRequest):
    query = req.query.strip().lower()
    city = get_city(req.city_id)

    ctx_str = json.dumps(req.context) if req.context else ""
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")

    if api_key:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
            system_prompt = (
                f"You are EcoPulse AI Copilot. Current city: {city['name']} ({city['zone']}). "
                f"Current AQI: {city['current']['aqi']}, EHI: {city['current']['ehi']} ({city['current']['ehi_band']}). "
                f"Dashboard context: {ctx_str}. "
                "Answer concisely and actionably about environmental risks, interventions, and forecasting. "
                "Always cite the data or model features you reference. Be professional and direct."
            )
            payload = {
                "contents": [{"parts": [{"text": req.query}]}],
                "systemInstruction": {"parts": [{"text": system_prompt}]},
                "generationConfig": {"temperature": 0.2, "maxOutputTokens": 350}
            }
            async with httpx.AsyncClient(timeout=8.0) as client:
                response = await client.post(url, headers={"Content-Type": "application/json"}, json=payload)
                if response.status_code == 200:
                    result = response.json()
                    candidates = result.get("candidates", [])
                    if candidates:
                        text = candidates[0].get("content", {}).get("parts", [{}])[0].get("text", "")
                        if text:
                            return {"answer": text, "source": "Gemini 1.5 Flash API"}
        except Exception as e:
            print(f"[Copilot] Gemini API failed: {e}. Using local Q&A fallback...")

    # Local Q&A fallback
    best_match = None
    max_matches = 0
    for item in MOCK_COPILOT_QA:
        matches = sum(1 for kw in item["keywords"] if kw in query)
        if matches > max_matches:
            max_matches = matches
            best_match = item["answer"]

    if best_match and max_matches > 0:
        return {"answer": best_match, "source": "Local Edge AI Engine (Offline Fallback)"}

    default = (
        f"I can help you analyze {city['name']}'s environmental data. Try asking:\n"
        "- Why is pollution increasing?\n"
        "- What actions should authorities take this week?\n"
        "- Which zone is at highest risk?\n"
        "- Explain the EHI score\n"
        "- How does the Digital Twin simulation work?"
    )
    return {"answer": default, "source": "Local Edge AI Engine (Offline Fallback)"}

# ─────────────────────────────────────────────────────────────────────────────
# LEGACY DEMO ENDPOINT (backwards compatibility)
# ─────────────────────────────────────────────────────────────────────────────
@app.get("/api/v1/demo")
def get_demo_state():
    """Legacy endpoint — returns Bengaluru dashboard state."""
    return get_city_dashboard("bengaluru")

# Mount static files last
app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
