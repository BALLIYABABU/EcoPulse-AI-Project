# EcoPulse AI
> **Predict. Explain. Prevent.**
> 
> Production-grade Command Center dashboard for environmental risk forecasting, explainable machine learning, and intervention planning. Built for the **SmartEarth Hackathon 2026** under the **Environmental Data Analytics Track**.

---

## 🗺️ Tiered Architecture Table (Technical Honesty Policy)

This demo is backed by **real running code** for all MVP features. We do not claim fake frontier model capabilities.

| Feature | MVP (Demo Day - Running Code) | Future Roadmap (Planned) |
| --- | --- | --- |
| **Forecasting** | **XGBoost Ensemble** (recursive forecasting with bootstrap residuals) | LSTM + TFT (Temporal Fusion Transformers) |
| **Geospatial Analysis** | **Preloaded NDVI diffs** (GeoJSON polygons with Leaflet overlays) | SegFormer on Sentinel-2 imagery |
| **Intervention Engine** | **Rule Engine + Priority Scoring** (Diminishing returns impact model) | Reinforcement Learning policy optimizer |
| **Explainability** | **SHAP on XGBoost** (`shap.TreeExplainer` local attributions) | LIME + Counterfactuals |
| **Copilot** | **Gemini 1.5 Flash API** + local edge Q&A fallback database | Fine-tuned LLM on local environmental policies |
| **Digital Twin** | **Parametric Scenario Simulation** (Instant client-side evaluation) | Physics-based fluid dynamics agent |

---

## 🏆 Competitive Edge (Why EcoPulse AI is Different)

While other teams focus solely on **monitoring**, EcoPulse AI is designed for **intervention**.

| System | Predicts | Explains | Intervenes | Simulates |
| --- | ---: | ---: | ---: | ---: |
| **SAFAR (IMD)** | ✓ | ✗ | ✗ | ✗ |
| **IQAir** | ✗ | ✗ | ✗ | ✗ |
| **Ambee** | ✓ | ✗ | ✗ | ✗ |
| **EcoPulse AI** | **✓** | **✓** | **✓** | **✓** |

---

## 📖 Primary Demo Story (Bengaluru Corridor)

* **City**: Bengaluru Industrial Corridor (Peenya–Whitefield Zone)
* **Time**: T+0 (Now)
* **Current Conditions**: AQI: 168 (Unhealthy) | Industrial Emissions: 74% | Traffic Density: 82% | Wind Speed: 1.2 m/s | Green Cover: 12%
* **Prediction (T+7)**: Projecting AQI to reach **287 (Hazardous)** with **91% confidence**. Composite EHI (Environmental Health Index) at **23/100 (Critical)**.
* **Root Cause (SHAP)**: Industrial Emissions (42% impact), Traffic Density (31%), Stagnant Weather (17%), Deforestation (10%).
* **Interventions Applied**:
  1. Reduce Peenya industrial output by 15% (AQI drop: 22% | Cost: ₹2.1 Cr)
  2. Restrict heavy vehicle traffic during peak hours (AQI drop: 18% | Cost: ₹0.4 Cr)
  3. Deploy 3km green corridor along corridor (AQI drop: 8% | Cost: ₹1.8 Cr)
* **Combined Outcome**: Averted Hazardous event! Projected AQI drops from **287 to 191** (Hazardous to Moderate/Poor), **protecting 43,000 residents**.

---

## 📂 Project Structure

```
ecopulse-ai/
├── data/
│   ├── bengaluru_aqi_12months.csv  # 12 months of CPCB data
│   ├── hotspot_clusters.geojson    # DBSCAN monitoring stations
│   ├── ndvi_change_bengaluru.geojson # Precomputed NDVI changes
│   ├── intervention_library.json   # 12 ranked administrative actions
│   └── shap_values_sample.json     # Precomputed SHAP values for T+0
├── static/
│   ├── index.html                  # Glassmorphic Landing + Dashboard UI
│   ├── style.css                   # Navy color system, pulsing glow animations
│   └── app.js                      # Chart.js, Leaflet map, twin simulator
├── ml_engine.py                    # XGBoost, SHAP Explainer, DBSCAN clustering
├── intervention_engine.py          # Cost-benefit scorer and impact engine
├── data_manager.py                 # Live OpenAQ fallback chain
├── main.py                         # FastAPI web server
├── generate_data.py                # Synthetic dataset & ML training script
├── test_backend.py                 # Automated unit tests
└── requirements.txt                # Dependencies
```

---

## ⚡ Setup & Run

### Prerequisites
* Python 3.13+ installed.

### Installation
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run data generator to train the models:
   ```bash
   python generate_data.py
   ```
3. Launch the FastAPI server:
   ```bash
   python -m uvicorn main:app --reload
   ```
4. Open your browser and navigate to:
   ```
   http://127.0.0.1:8000/
   ```

### Running Tests
To run unit tests:
```bash
python -m unittest test_backend.py
```
