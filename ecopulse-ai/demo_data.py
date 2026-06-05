# =============================================================================
# EcoPulse AI — Bundled Demo Data (Fully Offline)
# All data hardcoded. No external API calls required.
# Cities: Bengaluru, Delhi, Mumbai, Chennai, Hyderabad
# =============================================================================

CITIES = {
    "bengaluru": {
        "id": "bengaluru",
        "name": "Bengaluru",
        "zone": "Peenya–Whitefield Industrial Corridor",
        "lat": 12.9716, "lon": 77.5946,
        "current": {
            "aqi": 168, "pm25": 89.4, "pm10": 142.1,
            "no2": 67.3, "so2": 34.1, "co": 1.8, "o3": 44.2,
            "temperature": 28.5, "humidity": 55.0, "wind_speed": 1.2, "rainfall": 0.0,
            "industrial_emissions": 0.74, "traffic_density": 0.82, "vegetation_index": 0.12,
            "water_stress": 38.0, "heatwave_risk": 42.0, "vegetation_loss": 88.0,
            "ehi": 23.0, "ehi_band": "Critical",
            "status": "Unhealthy"
        },
        "forecast": [
            {"day": "T+0", "date": "Jun 05", "aqi": 168, "aqi_lower": 148, "aqi_upper": 188},
            {"day": "T+1", "date": "Jun 06", "aqi": 185, "aqi_lower": 162, "aqi_upper": 208},
            {"day": "T+2", "date": "Jun 07", "aqi": 201, "aqi_lower": 176, "aqi_upper": 226},
            {"day": "T+3", "date": "Jun 08", "aqi": 218, "aqi_lower": 190, "aqi_upper": 246},
            {"day": "T+4", "date": "Jun 09", "aqi": 241, "aqi_lower": 210, "aqi_upper": 272},
            {"day": "T+5", "date": "Jun 10", "aqi": 263, "aqi_lower": 229, "aqi_upper": 297},
            {"day": "T+6", "date": "Jun 11", "aqi": 287, "aqi_lower": 251, "aqi_upper": 316}
        ],
        "risk_probability": "91%",
        "risk_classification": "Hazardous",
        "max_forecast_aqi": 287,
        "shap_values": {
            "base_value": 114.2,
            "predicted_value": 168.0,
            "contributions": [
                {"feature": "industrial_emissions", "display_name": "Industrial Emissions", "feature_value": 0.74, "shap_value": 24.6},
                {"feature": "traffic_density", "display_name": "Traffic Density", "feature_value": 0.82, "shap_value": 18.9},
                {"feature": "wind_speed", "display_name": "Wind Speed (Stagnation)", "feature_value": 1.2, "shap_value": 14.2},
                {"feature": "vegetation_index", "display_name": "Vegetation Loss", "feature_value": 0.12, "shap_value": 7.8},
                {"feature": "pm10_lag1", "display_name": "PM10 Lag (1-day)", "feature_value": 138.0, "shap_value": 5.4},
                {"feature": "temperature", "display_name": "Temperature", "feature_value": 28.5, "shap_value": -3.1},
                {"feature": "humidity", "display_name": "Humidity", "feature_value": 55.0, "shap_value": -4.0}
            ]
        },
        "interventions": [
            {"id": "IND-001", "name": "Reduce Industrial Output 15% (Peenya)", "category": "industrial",
             "aqi_reduction_pct": 22, "cost_inr_cr": 2.1, "co2_reduction_tonnes": 340,
             "implementation_days": 3, "confidence": 0.89, "score": 9.21,
             "description": "Mandatory 15% production reduction for Peenya zone factories during high-pollution windows."},
            {"id": "TRF-001", "name": "Restrict Heavy Vehicles 6AM–10PM", "category": "traffic",
             "aqi_reduction_pct": 18, "cost_inr_cr": 0.4, "co2_reduction_tonnes": 185,
             "implementation_days": 1, "confidence": 0.84, "score": 8.85,
             "description": "Ban diesel heavy vehicles from arterial roads during peak pollution hours."},
            {"id": "GRN-001", "name": "3km Green Corridor – Peenya-Yeshwanthpur", "category": "vegetation",
             "aqi_reduction_pct": 8, "cost_inr_cr": 1.8, "co2_reduction_tonnes": 85,
             "implementation_days": 14, "confidence": 0.71, "score": 7.40,
             "description": "Emergency plantation of 12,000 native species along Peenya industrial boundary."},
            {"id": "TRF-002", "name": "Alternate Day Vehicle Scheme", "category": "traffic",
             "aqi_reduction_pct": 12, "cost_inr_cr": 0.2, "co2_reduction_tonnes": 120,
             "implementation_days": 2, "confidence": 0.77, "score": 7.10,
             "description": "Odd/even vehicle restriction for private vehicles in Whitefield and Outer Ring Road."},
            {"id": "IND-002", "name": "Stack Emission Filter Mandate", "category": "industrial",
             "aqi_reduction_pct": 9, "cost_inr_cr": 3.5, "co2_reduction_tonnes": 95,
             "implementation_days": 7, "confidence": 0.68, "score": 6.55,
             "description": "Mandate HEPA filtration on all industrial chimneys above 20m height."},
            {"id": "TRF-003", "name": "Emergency WFH Advisory – IT Corridor", "category": "traffic",
             "aqi_reduction_pct": 10, "cost_inr_cr": 0.1, "co2_reduction_tonnes": 70,
             "implementation_days": 1, "confidence": 0.81, "score": 6.20,
             "description": "Government advisory for 50% WFH in Whitefield/ITPL IT corridor."},
            {"id": "IND-003", "name": "Wet Dust Suppression – Construction Sites", "category": "industrial",
             "aqi_reduction_pct": 7, "cost_inr_cr": 0.6, "co2_reduction_tonnes": 40,
             "implementation_days": 2, "confidence": 0.74, "score": 5.80,
             "description": "Mandatory water sprinkling at all active construction zones."}
        ],
        "hotspots": [
            {"id": "ST-001", "name": "Peenya Industrial Sector (Core)", "type": "Industrial Zone",
             "lat": 13.027, "lon": 77.518, "aqi": 224, "pm25": 145.2, "pm10": 223.8, "no2": 88.2, "co": 3.2,
             "cluster": 0, "is_anomaly": False, "anomaly_type": None},
            {"id": "ST-002", "name": "Yeshwanthpur Junction", "type": "Traffic Hub",
             "lat": 13.017, "lon": 77.541, "aqi": 219, "pm25": 138.7, "pm10": 208.3, "no2": 82.1, "co": 2.8,
             "cluster": 0, "is_anomaly": False, "anomaly_type": None},
            {"id": "ST-003", "name": "Rajajinagar Monitor", "type": "Residential",
             "lat": 12.997, "lon": 77.552, "aqi": 187, "pm25": 112.1, "pm10": 178.4, "no2": 61.2, "co": 2.1,
             "cluster": 0, "is_anomaly": False, "anomaly_type": None},
            {"id": "ST-004", "name": "Whitefield ITPL Zone", "type": "IT Hub",
             "lat": 12.985, "lon": 77.741, "aqi": 198, "pm25": 121.3, "pm10": 189.2, "no2": 71.8, "co": 2.4,
             "cluster": 1, "is_anomaly": False, "anomaly_type": None},
            {"id": "ST-005", "name": "Bellandur Outer Ring", "type": "Residential-Commercial",
             "lat": 12.933, "lon": 77.676, "aqi": 205, "pm25": 127.8, "pm10": 196.4, "no2": 74.3, "co": 2.6,
             "cluster": 1, "is_anomaly": False, "anomaly_type": None},
            {"id": "ST-006", "name": "Hebbal North", "type": "Residential",
             "lat": 13.035, "lon": 77.596, "aqi": 143, "pm25": 87.2, "pm10": 132.1, "no2": 48.2, "co": 1.6,
             "cluster": -1, "is_anomaly": False, "anomaly_type": None},
            {"id": "ST-007", "name": "BTM Layout South", "type": "Residential",
             "lat": 12.916, "lon": 77.617, "aqi": 128, "pm25": 72.4, "pm10": 115.3, "no2": 42.1, "co": 1.4,
             "cluster": -1, "is_anomaly": False, "anomaly_type": None},
            {"id": "ST-016", "name": "Silk Board Monitor", "type": "Traffic Node",
             "lat": 12.918, "lon": 77.623, "aqi": 999, "pm25": 0.0, "pm10": 0.0, "no2": 0.0, "co": 0.0,
             "cluster": -1, "is_anomaly": True, "anomaly_type": "Sensor Spike Error – Out-of-bounds value"},
            {"id": "ST-017", "name": "ORR Station Monitor", "type": "Roadway",
             "lat": 12.960, "lon": 77.698, "aqi": 0, "pm25": 0.0, "pm10": 0.0, "no2": 0.0, "co": 0.0,
             "cluster": -1, "is_anomaly": True, "anomaly_type": "Connection Loss – Zero flatline reading"}
        ],
        "simulation_base": {
            "traffic": 82, "industrial": 74, "green": 12, "wind": 1.2, "rainfall": 0,
            "base_aqi": 203.2
        },
        "crisis_message": "XGBoost projects AQI to hit <strong>287 (Hazardous)</strong> within <strong>7 days</strong> due to stagnant weather &amp; high Peenya emissions. Exceedance Probability: <strong>91%</strong>."
    },

    "delhi": {
        "id": "delhi",
        "name": "Delhi NCR",
        "zone": "Anand Vihar–Wazirpur Industrial Belt",
        "lat": 28.6139, "lon": 77.2090,
        "current": {
            "aqi": 342, "pm25": 187.6, "pm10": 298.4,
            "no2": 112.1, "so2": 52.8, "co": 4.2, "o3": 38.1,
            "temperature": 38.2, "humidity": 31.0, "wind_speed": 0.8, "rainfall": 0.0,
            "industrial_emissions": 0.88, "traffic_density": 0.91, "vegetation_index": 0.06,
            "water_stress": 72.0, "heatwave_risk": 78.0, "vegetation_loss": 94.0,
            "ehi": 8.2, "ehi_band": "Emergency",
            "status": "Severe"
        },
        "forecast": [
            {"day": "T+0", "date": "Jun 05", "aqi": 342, "aqi_lower": 310, "aqi_upper": 374},
            {"day": "T+1", "date": "Jun 06", "aqi": 358, "aqi_lower": 322, "aqi_upper": 394},
            {"day": "T+2", "date": "Jun 07", "aqi": 371, "aqi_lower": 333, "aqi_upper": 409},
            {"day": "T+3", "date": "Jun 08", "aqi": 389, "aqi_lower": 349, "aqi_upper": 429},
            {"day": "T+4", "date": "Jun 09", "aqi": 401, "aqi_lower": 359, "aqi_upper": 443},
            {"day": "T+5", "date": "Jun 10", "aqi": 418, "aqi_lower": 374, "aqi_upper": 462},
            {"day": "T+6", "date": "Jun 11", "aqi": 432, "aqi_lower": 386, "aqi_upper": 478}
        ],
        "risk_probability": "98%",
        "risk_classification": "Hazardous",
        "max_forecast_aqi": 432,
        "shap_values": {
            "base_value": 198.4,
            "predicted_value": 342.0,
            "contributions": [
                {"feature": "industrial_emissions", "display_name": "Industrial Emissions", "feature_value": 0.88, "shap_value": 54.2},
                {"feature": "traffic_density", "display_name": "Traffic Density", "feature_value": 0.91, "shap_value": 48.7},
                {"feature": "wind_speed", "display_name": "Wind Speed (Stagnation)", "feature_value": 0.8, "shap_value": 31.4},
                {"feature": "vegetation_index", "display_name": "Vegetation Loss", "feature_value": 0.06, "shap_value": 18.2},
                {"feature": "temperature", "display_name": "Heatwave Temperature", "feature_value": 38.2, "shap_value": 12.1},
                {"feature": "pm10_lag1", "display_name": "PM10 Lag (1-day)", "feature_value": 284.0, "shap_value": 9.3},
                {"feature": "humidity", "display_name": "Low Humidity", "feature_value": 31.0, "shap_value": -4.2}
            ]
        },
        "interventions": [
            {"id": "DEL-IND-001", "name": "Wazirpur Factory Shutdown (72h)", "category": "industrial",
             "aqi_reduction_pct": 28, "cost_inr_cr": 8.4, "co2_reduction_tonnes": 620,
             "implementation_days": 1, "confidence": 0.92, "score": 9.84,
             "description": "Mandatory 72-hour shutdown of Wazirpur industrial units during GRAP Stage IV."},
            {"id": "DEL-TRF-001", "name": "Odd-Even Vehicle Scheme (Metro boost)", "category": "traffic",
             "aqi_reduction_pct": 22, "cost_inr_cr": 1.2, "co2_reduction_tonnes": 410,
             "implementation_days": 1, "confidence": 0.87, "score": 9.12,
             "description": "Strict odd-even enforcement with free metro services on affected days."},
            {"id": "DEL-AGR-001", "name": "Stubble Burning Ban (Punjab border)", "category": "agricultural",
             "aqi_reduction_pct": 18, "cost_inr_cr": 4.5, "co2_reduction_tonnes": 890,
             "implementation_days": 2, "confidence": 0.79, "score": 8.22,
             "description": "Deploy 1,200 farm management teams across Haryana-Punjab belt to prevent stubble burning."},
            {"id": "DEL-GRN-001", "name": "Anti-smog Water Spray Deployment", "category": "mitigation",
             "aqi_reduction_pct": 8, "cost_inr_cr": 0.8, "co2_reduction_tonnes": 0,
             "implementation_days": 1, "confidence": 0.62, "score": 5.90,
             "description": "Deploy anti-smog guns and water spray vehicles across Connaught Place and ITO."},
            {"id": "DEL-SCH-001", "name": "School/College Closure Advisory", "category": "public_health",
             "aqi_reduction_pct": 0, "cost_inr_cr": 0.0, "co2_reduction_tonnes": 35,
             "implementation_days": 1, "confidence": 0.97, "score": 9.50,
             "description": "Close all educational institutions and outdoor public gatherings during GRAP Stage IV."},
            {"id": "DEL-CON-001", "name": "Construction Work Ban (NCR-wide)", "category": "industrial",
             "aqi_reduction_pct": 12, "cost_inr_cr": 5.2, "co2_reduction_tonnes": 148,
             "implementation_days": 1, "confidence": 0.83, "score": 7.88,
             "description": "Stop all earthwork, excavation, and demolition activity across Delhi NCR boundaries."}
        ],
        "hotspots": [
            {"id": "DL-001", "name": "Anand Vihar Bus Terminal", "type": "Transport Hub",
             "lat": 28.647, "lon": 77.316, "aqi": 415, "pm25": 228.4, "pm10": 362.1, "no2": 132.5, "co": 5.8,
             "cluster": 0, "is_anomaly": False, "anomaly_type": None},
            {"id": "DL-002", "name": "Wazirpur Industrial Estate", "type": "Industrial Zone",
             "lat": 28.694, "lon": 77.162, "aqi": 398, "pm25": 214.7, "pm10": 338.9, "no2": 118.3, "co": 5.2,
             "cluster": 0, "is_anomaly": False, "anomaly_type": None},
            {"id": "DL-003", "name": "Rohini Sector 17", "type": "Residential",
             "lat": 28.737, "lon": 77.075, "aqi": 361, "pm25": 192.3, "pm10": 304.7, "no2": 98.6, "co": 4.4,
             "cluster": 1, "is_anomaly": False, "anomaly_type": None},
            {"id": "DL-004", "name": "ITO Junction", "type": "Traffic Node",
             "lat": 28.627, "lon": 77.245, "aqi": 378, "pm25": 201.2, "pm10": 318.4, "no2": 108.4, "co": 4.8,
             "cluster": 1, "is_anomaly": False, "anomaly_type": None},
            {"id": "DL-005", "name": "Lodhi Road Station", "type": "Residential",
             "lat": 28.591, "lon": 77.221, "aqi": 289, "pm25": 154.2, "pm10": 244.3, "no2": 81.2, "co": 3.4,
             "cluster": -1, "is_anomaly": False, "anomaly_type": None},
            {"id": "DL-016", "name": "Punjabi Bagh Sensor", "type": "Roadway",
             "lat": 28.668, "lon": 77.132, "aqi": 999, "pm25": 0.0, "pm10": 0.0, "no2": 0.0, "co": 0.0,
             "cluster": -1, "is_anomaly": True, "anomaly_type": "Calibration Drift – Reported value exceeds physical maximum"}
        ],
        "simulation_base": {
            "traffic": 91, "industrial": 88, "green": 6, "wind": 0.8, "rainfall": 0,
            "base_aqi": 280.0
        },
        "crisis_message": "XGBoost projects AQI to hit <strong>432 (Hazardous)</strong> within <strong>7 days</strong>. GRAP Stage IV mandatory. Exceedance Probability: <strong>98%</strong>."
    },

    "mumbai": {
        "id": "mumbai",
        "name": "Mumbai",
        "zone": "Dharavi–Chembur Industrial Harbor",
        "lat": 19.0760, "lon": 72.8777,
        "current": {
            "aqi": 145, "pm25": 78.2, "pm10": 124.3,
            "no2": 54.2, "so2": 28.7, "co": 1.4, "o3": 51.8,
            "temperature": 31.8, "humidity": 78.0, "wind_speed": 4.2, "rainfall": 8.0,
            "industrial_emissions": 0.56, "traffic_density": 0.74, "vegetation_index": 0.18,
            "water_stress": 22.0, "heatwave_risk": 35.0, "vegetation_loss": 82.0,
            "ehi": 34.2, "ehi_band": "Critical",
            "status": "Moderate"
        },
        "forecast": [
            {"day": "T+0", "date": "Jun 05", "aqi": 145, "aqi_lower": 128, "aqi_upper": 162},
            {"day": "T+1", "date": "Jun 06", "aqi": 152, "aqi_lower": 133, "aqi_upper": 171},
            {"day": "T+2", "date": "Jun 07", "aqi": 148, "aqi_lower": 130, "aqi_upper": 166},
            {"day": "T+3", "date": "Jun 08", "aqi": 163, "aqi_lower": 143, "aqi_upper": 183},
            {"day": "T+4", "date": "Jun 09", "aqi": 171, "aqi_lower": 150, "aqi_upper": 192},
            {"day": "T+5", "date": "Jun 10", "aqi": 179, "aqi_lower": 157, "aqi_upper": 201},
            {"day": "T+6", "date": "Jun 11", "aqi": 188, "aqi_lower": 165, "aqi_upper": 211}
        ],
        "risk_probability": "62%",
        "risk_classification": "High",
        "max_forecast_aqi": 188,
        "shap_values": {
            "base_value": 96.8,
            "predicted_value": 145.0,
            "contributions": [
                {"feature": "traffic_density", "display_name": "Traffic Density", "feature_value": 0.74, "shap_value": 21.3},
                {"feature": "industrial_emissions", "display_name": "Harbor Industrial Emissions", "feature_value": 0.56, "shap_value": 16.8},
                {"feature": "pm10_lag1", "display_name": "PM10 Lag (1-day)", "feature_value": 118.4, "shap_value": 9.2},
                {"feature": "wind_speed", "display_name": "Sea Breeze (Positive)", "feature_value": 4.2, "shap_value": -8.4},
                {"feature": "humidity", "display_name": "Monsoon Humidity", "feature_value": 78.0, "shap_value": -6.1},
                {"feature": "vegetation_index", "display_name": "Urban Green Cover", "feature_value": 0.18, "shap_value": 5.2},
                {"feature": "rainfall", "display_name": "Recent Rainfall", "feature_value": 8.0, "shap_value": -4.8}
            ]
        },
        "interventions": [
            {"id": "MUM-HAR-001", "name": "Restrict Old Diesel Trucks – Nhava Sheva", "category": "traffic",
             "aqi_reduction_pct": 16, "cost_inr_cr": 0.6, "co2_reduction_tonnes": 220,
             "implementation_days": 2, "confidence": 0.81, "score": 8.44,
             "description": "Ban pre-BS4 diesel trucks from Nhava Sheva port access roads during 8AM–8PM."},
            {"id": "MUM-IND-001", "name": "Chembur Refinery Emission Cap", "category": "industrial",
             "aqi_reduction_pct": 19, "cost_inr_cr": 3.8, "co2_reduction_tonnes": 380,
             "implementation_days": 3, "confidence": 0.84, "score": 8.92,
             "description": "Apply temporary 20% throughput reduction at Chembur petroleum processing units."},
            {"id": "MUM-GRN-001", "name": "Mangrove Restoration Buffer (Thane Creek)", "category": "vegetation",
             "aqi_reduction_pct": 6, "cost_inr_cr": 2.2, "co2_reduction_tonnes": 65,
             "implementation_days": 21, "confidence": 0.68, "score": 6.10,
             "description": "Emergency replanting of mangrove buffer along Thane Creek for long-term filtration."},
            {"id": "MUM-TRF-001", "name": "Western Express Highway HOV Lanes", "category": "traffic",
             "aqi_reduction_pct": 10, "cost_inr_cr": 0.3, "co2_reduction_tonnes": 90,
             "implementation_days": 1, "confidence": 0.76, "score": 7.22,
             "description": "Implement High Occupancy Vehicle restrictions on WEH between Dahisar and Mahim."},
            {"id": "MUM-CON-001", "name": "Coastal Road Dust Suppression", "category": "industrial",
             "aqi_reduction_pct": 5, "cost_inr_cr": 0.4, "co2_reduction_tonnes": 22,
             "implementation_days": 1, "confidence": 0.71, "score": 5.68,
             "description": "Mandatory water sprinkling every 4 hours at Coastal Road and Bandra-Worli construction."}
        ],
        "hotspots": [
            {"id": "MUM-001", "name": "Dharavi Slum-Industrial Boundary", "type": "Mixed Zone",
             "lat": 19.043, "lon": 72.854, "aqi": 192, "pm25": 112.4, "pm10": 178.1, "no2": 72.3, "co": 2.4,
             "cluster": 0, "is_anomaly": False, "anomaly_type": None},
            {"id": "MUM-002", "name": "Chembur Petroleum Belt", "type": "Industrial Zone",
             "lat": 19.064, "lon": 72.900, "aqi": 178, "pm25": 98.7, "pm10": 156.2, "no2": 64.8, "co": 2.1,
             "cluster": 0, "is_anomaly": False, "anomaly_type": None},
            {"id": "MUM-003", "name": "Bandra-Kurla Complex", "type": "Commercial Hub",
             "lat": 19.065, "lon": 72.868, "aqi": 138, "pm25": 74.2, "pm10": 112.8, "no2": 48.9, "co": 1.6,
             "cluster": -1, "is_anomaly": False, "anomaly_type": None},
            {"id": "MUM-004", "name": "Colaba Promenade", "type": "Coastal Residential",
             "lat": 18.908, "lon": 72.814, "aqi": 89, "pm25": 42.1, "pm10": 68.4, "no2": 28.2, "co": 0.9,
             "cluster": -1, "is_anomaly": False, "anomaly_type": None},
            {"id": "MUM-016", "name": "Andheri East Sensor", "type": "Roadway",
             "lat": 19.116, "lon": 72.871, "aqi": 0, "pm25": 0.0, "pm10": 0.0, "no2": 0.0, "co": 0.0,
             "cluster": -1, "is_anomaly": True, "anomaly_type": "Power Failure – Sensor offline since 18:00"}
        ],
        "simulation_base": {
            "traffic": 74, "industrial": 56, "green": 18, "wind": 4.2, "rainfall": 8,
            "base_aqi": 160.0
        },
        "crisis_message": "XGBoost projects AQI to reach <strong>188 (Unhealthy)</strong> within <strong>7 days</strong>. Monsoon sea breeze is providing partial relief. Exceedance Probability: <strong>62%</strong>."
    },

    "chennai": {
        "id": "chennai",
        "name": "Chennai",
        "zone": "Manali–Ennore Industrial Port Cluster",
        "lat": 13.0827, "lon": 80.2707,
        "current": {
            "aqi": 82, "pm25": 38.4, "pm10": 68.2,
            "no2": 32.1, "so2": 16.8, "co": 0.9, "o3": 58.4,
            "temperature": 33.4, "humidity": 68.0, "wind_speed": 5.8, "rainfall": 12.0,
            "industrial_emissions": 0.42, "traffic_density": 0.58, "vegetation_index": 0.24,
            "water_stress": 28.0, "heatwave_risk": 48.0, "vegetation_loss": 76.0,
            "ehi": 48.6, "ehi_band": "Stressed",
            "status": "Satisfactory"
        },
        "forecast": [
            {"day": "T+0", "date": "Jun 05", "aqi": 82, "aqi_lower": 68, "aqi_upper": 96},
            {"day": "T+1", "date": "Jun 06", "aqi": 88, "aqi_lower": 73, "aqi_upper": 103},
            {"day": "T+2", "date": "Jun 07", "aqi": 94, "aqi_lower": 78, "aqi_upper": 110},
            {"day": "T+3", "date": "Jun 08", "aqi": 102, "aqi_lower": 85, "aqi_upper": 119},
            {"day": "T+4", "date": "Jun 09", "aqi": 109, "aqi_lower": 91, "aqi_upper": 127},
            {"day": "T+5", "date": "Jun 10", "aqi": 118, "aqi_lower": 98, "aqi_upper": 138},
            {"day": "T+6", "date": "Jun 11", "aqi": 128, "aqi_lower": 106, "aqi_upper": 150}
        ],
        "risk_probability": "28%",
        "risk_classification": "Moderate",
        "max_forecast_aqi": 128,
        "shap_values": {
            "base_value": 62.1,
            "predicted_value": 82.0,
            "contributions": [
                {"feature": "industrial_emissions", "display_name": "Ennore Port Emissions", "feature_value": 0.42, "shap_value": 12.8},
                {"feature": "traffic_density", "display_name": "Traffic Density", "feature_value": 0.58, "shap_value": 9.4},
                {"feature": "wind_speed", "display_name": "Bay of Bengal Breeze", "feature_value": 5.8, "shap_value": -11.2},
                {"feature": "vegetation_index", "display_name": "Coastal Vegetation", "feature_value": 0.24, "shap_value": 4.1},
                {"feature": "rainfall", "display_name": "Pre-monsoon Rainfall", "feature_value": 12.0, "shap_value": -7.8},
                {"feature": "temperature", "display_name": "Temperature", "feature_value": 33.4, "shap_value": 6.2},
                {"feature": "humidity", "display_name": "Coastal Humidity", "feature_value": 68.0, "shap_value": -3.6}
            ]
        },
        "interventions": [
            {"id": "CHE-IND-001", "name": "Ennore Port Stack Emission Audit", "category": "industrial",
             "aqi_reduction_pct": 14, "cost_inr_cr": 1.8, "co2_reduction_tonnes": 180,
             "implementation_days": 5, "confidence": 0.78, "score": 7.88,
             "description": "Mandatory third-party emission audit and 10% reduction mandate for Ennore port industries."},
            {"id": "CHE-TRF-001", "name": "Coastal Road Freight Restriction", "category": "traffic",
             "aqi_reduction_pct": 10, "cost_inr_cr": 0.2, "co2_reduction_tonnes": 95,
             "implementation_days": 1, "confidence": 0.82, "score": 7.62,
             "description": "Restrict freight traffic on ECR and PCH during 7AM–10AM peak exposure windows."},
            {"id": "CHE-GRN-001", "name": "Manali Green Barrier Plantation", "category": "vegetation",
             "aqi_reduction_pct": 7, "cost_inr_cr": 1.4, "co2_reduction_tonnes": 58,
             "implementation_days": 14, "confidence": 0.65, "score": 6.22,
             "description": "Plant fast-growing native species along Manali industrial perimeter as pollution buffer."},
            {"id": "CHE-WAT-001", "name": "Pallikaranai Wetland Protection Order", "category": "ecosystem",
             "aqi_reduction_pct": 4, "cost_inr_cr": 0.5, "co2_reduction_tonnes": 42,
             "implementation_days": 7, "confidence": 0.88, "score": 6.84,
             "description": "Legal protection for Pallikaranai marshland to maintain natural air filtration function."}
        ],
        "hotspots": [
            {"id": "CHE-001", "name": "Manali Petrochemical Zone", "type": "Industrial Zone",
             "lat": 13.166, "lon": 80.258, "aqi": 142, "pm25": 78.4, "pm10": 124.2, "no2": 52.8, "co": 1.8,
             "cluster": 0, "is_anomaly": False, "anomaly_type": None},
            {"id": "CHE-002", "name": "Ennore Port Entry Gate", "type": "Port Terminal",
             "lat": 13.218, "lon": 80.326, "aqi": 124, "pm25": 64.2, "pm10": 98.6, "no2": 44.1, "co": 1.4,
             "cluster": 0, "is_anomaly": False, "anomaly_type": None},
            {"id": "CHE-003", "name": "Anna Nagar Residential", "type": "Residential",
             "lat": 13.087, "lon": 80.208, "aqi": 72, "pm25": 32.1, "pm10": 58.4, "no2": 24.2, "co": 0.7,
             "cluster": -1, "is_anomaly": False, "anomaly_type": None},
            {"id": "CHE-004", "name": "Marina Beach Promenade", "type": "Coastal Park",
             "lat": 13.050, "lon": 80.282, "aqi": 44, "pm25": 18.2, "pm10": 34.1, "no2": 14.2, "co": 0.3,
             "cluster": -1, "is_anomaly": False, "anomaly_type": None}
        ],
        "simulation_base": {
            "traffic": 58, "industrial": 42, "green": 24, "wind": 5.8, "rainfall": 12,
            "base_aqi": 120.0
        },
        "crisis_message": "Conditions are currently <strong>Satisfactory</strong>. XGBoost forecasts a gradual rise to <strong>128 AQI (Moderate)</strong> over 7 days. Proactive action recommended. Probability: <strong>28%</strong>."
    },

    "hyderabad": {
        "id": "hyderabad",
        "name": "Hyderabad",
        "zone": "Patancheru–Bollaram Chemical Corridor",
        "lat": 17.3850, "lon": 78.4867,
        "current": {
            "aqi": 124, "pm25": 64.8, "pm10": 108.4,
            "no2": 48.2, "so2": 24.6, "co": 1.2, "o3": 47.9,
            "temperature": 35.2, "humidity": 42.0, "wind_speed": 2.8, "rainfall": 0.0,
            "industrial_emissions": 0.61, "traffic_density": 0.68, "vegetation_index": 0.16,
            "water_stress": 52.0, "heatwave_risk": 62.0, "vegetation_loss": 84.0,
            "ehi": 29.8, "ehi_band": "Critical",
            "status": "Moderate"
        },
        "forecast": [
            {"day": "T+0", "date": "Jun 05", "aqi": 124, "aqi_lower": 108, "aqi_upper": 140},
            {"day": "T+1", "date": "Jun 06", "aqi": 138, "aqi_lower": 120, "aqi_upper": 156},
            {"day": "T+2", "date": "Jun 07", "aqi": 151, "aqi_lower": 132, "aqi_upper": 170},
            {"day": "T+3", "date": "Jun 08", "aqi": 162, "aqi_lower": 141, "aqi_upper": 183},
            {"day": "T+4", "date": "Jun 09", "aqi": 178, "aqi_lower": 155, "aqi_upper": 201},
            {"day": "T+5", "date": "Jun 10", "aqi": 194, "aqi_lower": 169, "aqi_upper": 219},
            {"day": "T+6", "date": "Jun 11", "aqi": 214, "aqi_lower": 186, "aqi_upper": 242}
        ],
        "risk_probability": "74%",
        "risk_classification": "Hazardous",
        "max_forecast_aqi": 214,
        "shap_values": {
            "base_value": 78.4,
            "predicted_value": 124.0,
            "contributions": [
                {"feature": "industrial_emissions", "display_name": "Patancheru Chemical Emissions", "feature_value": 0.61, "shap_value": 18.4},
                {"feature": "traffic_density", "display_name": "Outer Ring Road Traffic", "feature_value": 0.68, "shap_value": 14.2},
                {"feature": "heatwave_risk", "display_name": "Heatwave Stress", "feature_value": 62.0, "shap_value": 11.8},
                {"feature": "wind_speed", "display_name": "Wind Stagnation", "feature_value": 2.8, "shap_value": 8.2},
                {"feature": "vegetation_index", "display_name": "Vegetation Cover", "feature_value": 0.16, "shap_value": 5.6},
                {"feature": "pm10_lag1", "display_name": "PM10 Lag (1-day)", "feature_value": 102.4, "shap_value": 4.2},
                {"feature": "humidity", "display_name": "Low Humidity", "feature_value": 42.0, "shap_value": -3.8}
            ]
        },
        "interventions": [
            {"id": "HYD-IND-001", "name": "Patancheru Chemical Plant Curtailment", "category": "industrial",
             "aqi_reduction_pct": 20, "cost_inr_cr": 3.2, "co2_reduction_tonnes": 285,
             "implementation_days": 2, "confidence": 0.86, "score": 9.02,
             "description": "Mandatory 20% production cut at Patancheru Special Economic Zone chemical units."},
            {"id": "HYD-TRF-001", "name": "Outer Ring Road Freight Timing Control", "category": "traffic",
             "aqi_reduction_pct": 13, "cost_inr_cr": 0.3, "co2_reduction_tonnes": 128,
             "implementation_days": 1, "confidence": 0.80, "score": 8.14,
             "description": "Shift heavy freight to 10PM–5AM window on HMDA Outer Ring Road."},
            {"id": "HYD-WAT-001", "name": "Hussain Sagar Lake Bioremediation", "category": "ecosystem",
             "aqi_reduction_pct": 3, "cost_inr_cr": 1.6, "co2_reduction_tonnes": 28,
             "implementation_days": 30, "confidence": 0.61, "score": 5.44,
             "description": "Accelerate bioremediation of Hussain Sagar to reduce methane and particulate release."},
            {"id": "HYD-GRN-001", "name": "Bollaram Industrial Green Wall", "category": "vegetation",
             "aqi_reduction_pct": 8, "cost_inr_cr": 1.1, "co2_reduction_tonnes": 62,
             "implementation_days": 10, "confidence": 0.70, "score": 6.88,
             "description": "Install 8km green wall of native shrubs along Bollaram industrial zone perimeter."},
            {"id": "HYD-TRF-002", "name": "MMTS Rail Incentive (Free Pass Scheme)", "category": "traffic",
             "aqi_reduction_pct": 9, "cost_inr_cr": 0.7, "co2_reduction_tonnes": 88,
             "implementation_days": 1, "confidence": 0.73, "score": 7.12,
             "description": "Issue free MMTS/Metro passes during high-pollution days to shift commuters off roads."}
        ],
        "hotspots": [
            {"id": "HYD-001", "name": "Patancheru Industrial Area", "type": "Chemical Zone",
             "lat": 17.527, "lon": 78.264, "aqi": 187, "pm25": 102.4, "pm10": 164.2, "no2": 68.4, "co": 2.2,
             "cluster": 0, "is_anomaly": False, "anomaly_type": None},
            {"id": "HYD-002", "name": "Bollaram Industrial Estate", "type": "Industrial Zone",
             "lat": 17.502, "lon": 78.322, "aqi": 168, "pm25": 88.2, "pm10": 142.6, "no2": 58.1, "co": 1.9,
             "cluster": 0, "is_anomaly": False, "anomaly_type": None},
            {"id": "HYD-003", "name": "Hitech City Madhapur", "type": "IT Hub",
             "lat": 17.447, "lon": 78.381, "aqi": 118, "pm25": 58.4, "pm10": 94.2, "no2": 42.1, "co": 1.2,
             "cluster": -1, "is_anomaly": False, "anomaly_type": None},
            {"id": "HYD-004", "name": "Banjara Hills Residential", "type": "Residential",
             "lat": 17.415, "lon": 78.449, "aqi": 98, "pm25": 44.2, "pm10": 76.8, "no2": 32.4, "co": 0.8,
             "cluster": -1, "is_anomaly": False, "anomaly_type": None},
            {"id": "HYD-016", "name": "ICRISAT Campus Monitor", "type": "Research Campus",
             "lat": 17.532, "lon": 78.274, "aqi": 999, "pm25": 0.0, "pm10": 0.0, "no2": 0.0, "co": 0.0,
             "cluster": -1, "is_anomaly": True, "anomaly_type": "Firmware Error – Device requires recalibration"}
        ],
        "simulation_base": {
            "traffic": 68, "industrial": 61, "green": 16, "wind": 2.8, "rainfall": 0,
            "base_aqi": 175.0
        },
        "crisis_message": "XGBoost projects AQI to cross <strong>200 (Hazardous)</strong> in <strong>7 days</strong>. Chemical corridor emissions are the primary driver. Exceedance Probability: <strong>74%</strong>."
    }
}


def get_city(city_id: str) -> dict:
    """Return city data by ID, fallback to bengaluru if not found."""
    return CITIES.get(city_id.lower(), CITIES["bengaluru"])


def list_cities() -> list:
    """Return summary list of all cities."""
    return [
        {
            "id": c["id"],
            "name": c["name"],
            "zone": c["zone"],
            "aqi": c["current"]["aqi"],
            "ehi": c["current"]["ehi"],
            "ehi_band": c["current"]["ehi_band"],
            "status": c["current"]["status"],
            "lat": c["lat"],
            "lon": c["lon"],
            "risk_probability": c["risk_probability"],
            "risk_classification": c["risk_classification"]
        }
        for c in CITIES.values()
    ]
