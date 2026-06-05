// =============================================================================
// EcoPulse AI — Frontend Application Controller v2.0
// Multi-city support, offline fallback, Chart.js, Leaflet, Copilot
// =============================================================================

// ─────────────────────────────────────────────────────────────────────────────
// OFFLINE FALLBACK DATA — ensures dashboard ALWAYS has something to display
// ─────────────────────────────────────────────────────────────────────────────
const OFFLINE_CITIES = {
  bengaluru: {
    city_id: "bengaluru", city: "Bengaluru", zone: "Peenya–Whitefield Industrial Corridor",
    lat: 12.9716, lon: 77.5946,
    current_conditions: { aqi: 168, pm25: 89.4, pm10: 142.1, no2: 67.3, so2: 34.1, co: 1.8, o3: 44.2, temperature: 28.5, humidity: 55, wind_speed: 1.2, rainfall: 0, ehi: 23.0, ehi_band: "Critical", status: "Unhealthy" },
    forecast_summary: {
      risk_probability: "91%", risk_classification: "Hazardous", max_forecast_aqi: 287,
      forecast: [
        { day: "T+0", date: "Jun 05", aqi: 168, aqi_lower: 148, aqi_upper: 188 },
        { day: "T+1", date: "Jun 06", aqi: 185, aqi_lower: 162, aqi_upper: 208 },
        { day: "T+2", date: "Jun 07", aqi: 201, aqi_lower: 176, aqi_upper: 226 },
        { day: "T+3", date: "Jun 08", aqi: 218, aqi_lower: 190, aqi_upper: 246 },
        { day: "T+4", date: "Jun 09", aqi: 241, aqi_lower: 210, aqi_upper: 272 },
        { day: "T+5", date: "Jun 10", aqi: 263, aqi_lower: 229, aqi_upper: 297 },
        { day: "T+6", date: "Jun 11", aqi: 287, aqi_lower: 251, aqi_upper: 316 }
      ]
    },
    shap_values: { base_value: 114.2, predicted_value: 168.0, contributions: [
      { feature: "industrial_emissions", display_name: "Industrial Emissions", feature_value: 0.74, shap_value: 24.6 },
      { feature: "traffic_density", display_name: "Traffic Density", feature_value: 0.82, shap_value: 18.9 },
      { feature: "wind_speed", display_name: "Wind Speed (Stagnation)", feature_value: 1.2, shap_value: 14.2 },
      { feature: "vegetation_index", display_name: "Vegetation Loss", feature_value: 0.12, shap_value: 7.8 },
      { feature: "pm10_lag1", display_name: "PM10 Lag (1-day)", feature_value: 138.0, shap_value: 5.4 },
      { feature: "temperature", display_name: "Temperature", feature_value: 28.5, shap_value: -3.1 }
    ]},
    interventions: [
      { id: "IND-001", name: "Reduce Industrial Output 15% (Peenya)", category: "industrial", aqi_reduction_pct: 22, cost_inr_cr: 2.1, co2_reduction_tonnes: 340, implementation_days: 3, confidence: 0.89, score: 9.21 },
      { id: "TRF-001", name: "Restrict Heavy Vehicles 6AM–10PM", category: "traffic", aqi_reduction_pct: 18, cost_inr_cr: 0.4, co2_reduction_tonnes: 185, implementation_days: 1, confidence: 0.84, score: 8.85 },
      { id: "GRN-001", name: "3km Green Corridor – Peenya-Yeshwanthpur", category: "vegetation", aqi_reduction_pct: 8, cost_inr_cr: 1.8, co2_reduction_tonnes: 85, implementation_days: 14, confidence: 0.71, score: 7.40 },
      { id: "TRF-002", name: "Alternate Day Vehicle Scheme", category: "traffic", aqi_reduction_pct: 12, cost_inr_cr: 0.2, co2_reduction_tonnes: 120, implementation_days: 2, confidence: 0.77, score: 7.10 },
      { id: "IND-002", name: "Stack Emission Filter Mandate", category: "industrial", aqi_reduction_pct: 9, cost_inr_cr: 3.5, co2_reduction_tonnes: 95, implementation_days: 7, confidence: 0.68, score: 6.55 }
    ],
    hotspots: [
      { id: "ST-001", name: "Peenya Industrial (Core)", type: "Industrial Zone", lat: 13.027, lon: 77.518, aqi: 224, pm25: 145.2, pm10: 223.8, no2: 88.2, co: 3.2, cluster: 0, is_anomaly: false, anomaly_type: null },
      { id: "ST-002", name: "Yeshwanthpur Junction", type: "Traffic Hub", lat: 13.017, lon: 77.541, aqi: 219, pm25: 138.7, pm10: 208.3, no2: 82.1, co: 2.8, cluster: 0, is_anomaly: false, anomaly_type: null },
      { id: "ST-003", name: "Rajajinagar Monitor", type: "Residential", lat: 12.997, lon: 77.552, aqi: 187, pm25: 112.1, pm10: 178.4, no2: 61.2, co: 2.1, cluster: 0, is_anomaly: false, anomaly_type: null },
      { id: "ST-004", name: "Whitefield ITPL Zone", type: "IT Hub", lat: 12.985, lon: 77.741, aqi: 198, pm25: 121.3, pm10: 189.2, no2: 71.8, co: 2.4, cluster: 1, is_anomaly: false, anomaly_type: null },
      { id: "ST-005", name: "Bellandur Outer Ring", type: "Residential", lat: 12.933, lon: 77.676, aqi: 205, pm25: 127.8, pm10: 196.4, no2: 74.3, co: 2.6, cluster: 1, is_anomaly: false, anomaly_type: null },
      { id: "ST-016", name: "Silk Board Monitor", type: "Traffic Node", lat: 12.918, lon: 77.623, aqi: 999, pm25: 0, pm10: 0, no2: 0, co: 0, cluster: -1, is_anomaly: true, anomaly_type: "Sensor Spike Error – Out-of-bounds value" },
      { id: "ST-017", name: "ORR Station Monitor", type: "Roadway", lat: 12.960, lon: 77.698, aqi: 0, pm25: 0, pm10: 0, no2: 0, co: 0, cluster: -1, is_anomaly: true, anomaly_type: "Connection Loss – Zero flatline reading" }
    ],
    simulation_base: { traffic: 82, industrial: 74, green: 12, wind: 1.2, rainfall: 0, base_aqi: 203.2 },
    crisis_message: "XGBoost projects AQI to hit <strong>287 (Hazardous)</strong> within <strong>7 days</strong> due to stagnant weather &amp; high Peenya emissions. Exceedance Probability: <strong>91%</strong>."
  },
  delhi: JSON.parse('{"city_id":"delhi","city":"Delhi NCR","zone":"Anand Vihar–Wazirpur Industrial Belt","lat":28.6139,"lon":77.209,"current_conditions":{"aqi":342,"pm25":187.6,"pm10":298.4,"no2":112.1,"so2":52.8,"co":4.2,"o3":38.1,"temperature":38.2,"humidity":31.0,"wind_speed":0.8,"rainfall":0.0,"ehi":8.2,"ehi_band":"Emergency","status":"Severe"},"forecast_summary":{"risk_probability":"98%","risk_classification":"Hazardous","max_forecast_aqi":432,"forecast":[{"day":"T+0","date":"Jun 05","aqi":342,"aqi_lower":310,"aqi_upper":374},{"day":"T+1","date":"Jun 06","aqi":358,"aqi_lower":322,"aqi_upper":394},{"day":"T+2","date":"Jun 07","aqi":371,"aqi_lower":333,"aqi_upper":409},{"day":"T+3","date":"Jun 08","aqi":389,"aqi_lower":349,"aqi_upper":429},{"day":"T+4","date":"Jun 09","aqi":401,"aqi_lower":359,"aqi_upper":443},{"day":"T+5","date":"Jun 10","aqi":418,"aqi_lower":374,"aqi_upper":462},{"day":"T+6","date":"Jun 11","aqi":432,"aqi_lower":386,"aqi_upper":478}]},"shap_values":{"base_value":198.4,"predicted_value":342.0,"contributions":[{"feature":"industrial_emissions","display_name":"Industrial Emissions","feature_value":0.88,"shap_value":54.2},{"feature":"traffic_density","display_name":"Traffic Density","feature_value":0.91,"shap_value":48.7},{"feature":"wind_speed","display_name":"Wind Speed (Stagnation)","feature_value":0.8,"shap_value":31.4},{"feature":"vegetation_index","display_name":"Vegetation Loss","feature_value":0.06,"shap_value":18.2},{"feature":"temperature","display_name":"Heatwave Temperature","feature_value":38.2,"shap_value":12.1},{"feature":"pm10_lag1","display_name":"PM10 Lag (1-day)","feature_value":284.0,"shap_value":9.3},{"feature":"humidity","display_name":"Low Humidity","feature_value":31.0,"shap_value":-4.2}]},"interventions":[{"id":"DEL-IND-001","name":"Wazirpur Factory Shutdown (72h)","category":"industrial","aqi_reduction_pct":28,"cost_inr_cr":8.4,"co2_reduction_tonnes":620,"implementation_days":1,"confidence":0.92,"score":9.84,"description":"Mandatory 72-hour shutdown of Wazirpur industrial units during GRAP Stage IV."},{"id":"DEL-TRF-001","name":"Odd-Even Vehicle Scheme (Metro boost)","category":"traffic","aqi_reduction_pct":22,"cost_inr_cr":1.2,"co2_reduction_tonnes":410,"implementation_days":1,"confidence":0.87,"score":9.12,"description":"Strict odd-even enforcement with free metro services on affected days."},{"id":"DEL-AGR-001","name":"Stubble Burning Ban (Punjab border)","category":"agricultural","aqi_reduction_pct":18,"cost_inr_cr":4.5,"co2_reduction_tonnes":890,"implementation_days":2,"confidence":0.79,"score":8.22,"description":"Deploy 1,200 farm management teams across Haryana-Punjab belt to prevent stubble burning."},{"id":"DEL-GRN-001","name":"Anti-smog Water Spray Deployment","category":"mitigation","aqi_reduction_pct":8,"cost_inr_cr":0.8,"co2_reduction_tonnes":0,"implementation_days":1,"confidence":0.62,"score":5.9,"description":"Deploy anti-smog guns and water spray vehicles across Connaught Place and ITO."},{"id":"DEL-SCH-001","name":"School/College Closure Advisory","category":"public_health","aqi_reduction_pct":0,"cost_inr_cr":0.0,"co2_reduction_tonnes":35,"implementation_days":1,"confidence":0.97,"score":9.5,"description":"Close all educational institutions and outdoor public gatherings during GRAP Stage IV."},{"id":"DEL-CON-001","name":"Construction Work Ban (NCR-wide)","category":"industrial","aqi_reduction_pct":12,"cost_inr_cr":5.2,"co2_reduction_tonnes":148,"implementation_days":1,"confidence":0.83,"score":7.88,"description":"Stop all earthwork, excavation, and demolition activity across Delhi NCR boundaries."}],"hotspots":[{"id":"DL-001","name":"Anand Vihar Bus Terminal","type":"Transport Hub","lat":28.647,"lon":77.316,"aqi":415,"pm25":228.4,"pm10":362.1,"no2":132.5,"co":5.8,"cluster":0,"is_anomaly":false,"anomaly_type":null},{"id":"DL-002","name":"Wazirpur Industrial Estate","type":"Industrial Zone","lat":28.694,"lon":77.162,"aqi":398,"pm25":214.7,"pm10":338.9,"no2":118.3,"co":5.2,"cluster":0,"is_anomaly":false,"anomaly_type":null},{"id":"DL-003","name":"Rohini Sector 17","type":"Residential","lat":28.737,"lon":77.075,"aqi":361,"pm25":192.3,"pm10":304.7,"no2":98.6,"co":4.4,"cluster":1,"is_anomaly":false,"anomaly_type":null},{"id":"DL-004","name":"ITO Junction","type":"Traffic Node","lat":28.627,"lon":77.245,"aqi":378,"pm25":201.2,"pm10":318.4,"no2":108.4,"co":4.8,"cluster":1,"is_anomaly":false,"anomaly_type":null},{"id":"DL-005","name":"Lodhi Road Station","type":"Residential","lat":28.591,"lon":77.221,"aqi":289,"pm25":154.2,"pm10":244.3,"no2":81.2,"co":3.4,"cluster":-1,"is_anomaly":false,"anomaly_type":null},{"id":"DL-016","name":"Punjabi Bagh Sensor","type":"Roadway","lat":28.668,"lon":77.132,"aqi":999,"pm25":0.0,"pm10":0.0,"no2":0.0,"co":0.0,"cluster":-1,"is_anomaly":true,"anomaly_type":"Calibration Drift – Reported value exceeds physical maximum"}],"simulation_base":{"traffic":91,"industrial":88,"green":6,"wind":0.8,"rainfall":0,"base_aqi":280.0},"crisis_message":"XGBoost projects AQI to hit <strong>432 (Hazardous)</strong> within <strong>7 days</strong>. GRAP Stage IV mandatory. Exceedance Probability: <strong>98%</strong>."}'),
  mumbai: JSON.parse('{"city_id":"mumbai","city":"Mumbai","zone":"Dharavi–Chembur Industrial Harbor","lat":19.076,"lon":72.8777,"current_conditions":{"aqi":145,"pm25":78.2,"pm10":124.3,"no2":54.2,"so2":28.7,"co":1.4,"o3":51.8,"temperature":31.8,"humidity":78.0,"wind_speed":4.2,"rainfall":8.0,"ehi":34.2,"ehi_band":"Critical","status":"Moderate"},"forecast_summary":{"risk_probability":"62%","risk_classification":"High","max_forecast_aqi":188,"forecast":[{"day":"T+0","date":"Jun 05","aqi":145,"aqi_lower":128,"aqi_upper":162},{"day":"T+1","date":"Jun 06","aqi":152,"aqi_lower":133,"aqi_upper":171},{"day":"T+2","date":"Jun 07","aqi":148,"aqi_lower":130,"aqi_upper":166},{"day":"T+3","date":"Jun 08","aqi":163,"aqi_lower":143,"aqi_upper":183},{"day":"T+4","date":"Jun 09","aqi":171,"aqi_lower":150,"aqi_upper":192},{"day":"T+5","date":"Jun 10","aqi":179,"aqi_lower":157,"aqi_upper":201},{"day":"T+6","date":"Jun 11","aqi":188,"aqi_lower":165,"aqi_upper":211}]},"shap_values":{"base_value":96.8,"predicted_value":145.0,"contributions":[{"feature":"traffic_density","display_name":"Traffic Density","feature_value":0.74,"shap_value":21.3},{"feature":"industrial_emissions","display_name":"Harbor Industrial Emissions","feature_value":0.56,"shap_value":16.8},{"feature":"pm10_lag1","display_name":"PM10 Lag (1-day)","feature_value":118.4,"shap_value":9.2},{"feature":"wind_speed","display_name":"Sea Breeze (Positive)","feature_value":4.2,"shap_value":-8.4},{"feature":"humidity","display_name":"Monsoon Humidity","feature_value":78.0,"shap_value":-6.1},{"feature":"vegetation_index","display_name":"Urban Green Cover","feature_value":0.18,"shap_value":5.2},{"feature":"rainfall","display_name":"Recent Rainfall","feature_value":8.0,"shap_value":-4.8}]},"interventions":[{"id":"MUM-HAR-001","name":"Restrict Old Diesel Trucks – Nhava Sheva","category":"traffic","aqi_reduction_pct":16,"cost_inr_cr":0.6,"co2_reduction_tonnes":220,"implementation_days":2,"confidence":0.81,"score":8.44,"description":"Ban pre-BS4 diesel trucks from Nhava Sheva port access roads during 8AM–8PM."},{"id":"MUM-IND-001","name":"Chembur Refinery Emission Cap","category":"industrial","aqi_reduction_pct":19,"cost_inr_cr":3.8,"co2_reduction_tonnes":380,"implementation_days":3,"confidence":0.84,"score":8.92,"description":"Apply temporary 20% throughput reduction at Chembur petroleum processing units."},{"id":"MUM-GRN-001","name":"Mangrove Restoration Buffer (Thane Creek)","category":"vegetation","aqi_reduction_pct":6,"cost_inr_cr":2.2,"co2_reduction_tonnes":65,"implementation_days":21,"confidence":0.68,"score":6.1,"description":"Emergency replanting of mangrove buffer along Thane Creek for long-term filtration."},{"id":"MUM-TRF-001","name":"Western Express Highway HOV Lanes","category":"traffic","aqi_reduction_pct":10,"cost_inr_cr":0.3,"co2_reduction_tonnes":90,"implementation_days":1,"confidence":0.76,"score":7.22,"description":"Implement High Occupancy Vehicle restrictions on WEH between Dahisar and Mahim."},{"id":"MUM-CON-001","name":"Coastal Road Dust Suppression","category":"industrial","aqi_reduction_pct":5,"cost_inr_cr":0.4,"co2_reduction_tonnes":22,"implementation_days":1,"confidence":0.71,"score":5.68,"description":"Mandatory water sprinkling every 4 hours at Coastal Road and Bandra-Worli construction."}],"hotspots":[{"id":"MUM-001","name":"Dharavi Slum-Industrial Boundary","type":"Mixed Zone","lat":19.043,"lon":72.854,"aqi":192,"pm25":112.4,"pm10":178.1,"no2":72.3,"co":2.4,"cluster":0,"is_anomaly":false,"anomaly_type":null},{"id":"MUM-002","name":"Chembur Petroleum Belt","type":"Industrial Zone","lat":19.064,"lon":72.9,"aqi":178,"pm25":98.7,"pm10":156.2,"no2":64.8,"co":2.1,"cluster":0,"is_anomaly":false,"anomaly_type":null},{"id":"MUM-003","name":"Bandra-Kurla Complex","type":"Commercial Hub","lat":19.065,"lon":72.868,"aqi":138,"pm25":74.2,"pm10":112.8,"no2":48.9,"co":1.6,"cluster":-1,"is_anomaly":false,"anomaly_type":null},{"id":"MUM-004","name":"Colaba Promenade","type":"Coastal Residential","lat":18.908,"lon":72.814,"aqi":89,"pm25":42.1,"pm10":68.4,"no2":28.2,"co":0.9,"cluster":-1,"is_anomaly":false,"anomaly_type":null},{"id":"MUM-016","name":"Andheri East Sensor","type":"Roadway","lat":19.116,"lon":72.871,"aqi":0,"pm25":0.0,"pm10":0.0,"no2":0.0,"co":0.0,"cluster":-1,"is_anomaly":true,"anomaly_type":"Power Failure – Sensor offline since 18:00"}],"simulation_base":{"traffic":74,"industrial":56,"green":18,"wind":4.2,"rainfall":8,"base_aqi":160.0},"crisis_message":"XGBoost projects AQI to reach <strong>188 (Unhealthy)</strong> within <strong>7 days</strong>. Monsoon sea breeze is providing partial relief. Exceedance Probability: <strong>62%</strong>."}'),
  chennai: JSON.parse('{"city_id":"chennai","city":"Chennai","zone":"Manali–Ennore Industrial Port Cluster","lat":13.0827,"lon":80.2707,"current_conditions":{"aqi":82,"pm25":38.4,"pm10":68.2,"no2":32.1,"so2":16.8,"co":0.9,"o3":58.4,"temperature":33.4,"humidity":68.0,"wind_speed":5.8,"rainfall":12.0,"ehi":48.6,"ehi_band":"Stressed","status":"Satisfactory"},"forecast_summary":{"risk_probability":"28%","risk_classification":"Moderate","max_forecast_aqi":128,"forecast":[{"day":"T+0","date":"Jun 05","aqi":82,"aqi_lower":68,"aqi_upper":96},{"day":"T+1","date":"Jun 06","aqi":88,"aqi_lower":73,"aqi_upper":103},{"day":"T+2","date":"Jun 07","aqi":94,"aqi_lower":78,"aqi_upper":110},{"day":"T+3","date":"Jun 08","aqi":102,"aqi_lower":85,"aqi_upper":119},{"day":"T+4","date":"Jun 09","aqi":109,"aqi_lower":91,"aqi_upper":127},{"day":"T+5","date":"Jun 10","aqi":118,"aqi_lower":98,"aqi_upper":138},{"day":"T+6","date":"Jun 11","aqi":128,"aqi_lower":106,"aqi_upper":150}]},"shap_values":{"base_value":62.1,"predicted_value":82.0,"contributions":[{"feature":"industrial_emissions","display_name":"Ennore Port Emissions","feature_value":0.42,"shap_value":12.8},{"feature":"traffic_density","display_name":"Traffic Density","feature_value":0.58,"shap_value":9.4},{"feature":"wind_speed","display_name":"Bay of Bengal Breeze","feature_value":5.8,"shap_value":-11.2},{"feature":"vegetation_index","display_name":"Coastal Vegetation","feature_value":0.24,"shap_value":4.1},{"feature":"rainfall","display_name":"Pre-monsoon Rainfall","feature_value":12.0,"shap_value":-7.8},{"feature":"temperature","display_name":"Temperature","feature_value":33.4,"shap_value":6.2},{"feature":"humidity","display_name":"Coastal Humidity","feature_value":68.0,"shap_value":-3.6}]},"interventions":[{"id":"CHE-IND-001","name":"Ennore Port Stack Emission Audit","category":"industrial","aqi_reduction_pct":14,"cost_inr_cr":1.8,"co2_reduction_tonnes":180,"implementation_days":5,"confidence":0.78,"score":7.88,"description":"Mandatory third-party emission audit and 10% reduction mandate for Ennore port industries."},{"id":"CHE-TRF-001","name":"Coastal Road Freight Restriction","category":"traffic","aqi_reduction_pct":10,"cost_inr_cr":0.2,"co2_reduction_tonnes":95,"implementation_days":1,"confidence":0.82,"score":7.62,"description":"Restrict freight traffic on ECR and PCH during 7AM–10AM peak exposure windows."},{"id":"CHE-GRN-001","name":"Manali Green Barrier Plantation","category":"vegetation","aqi_reduction_pct":7,"cost_inr_cr":1.4,"co2_reduction_tonnes":58,"implementation_days":14,"confidence":0.65,"score":6.22,"description":"Plant fast-growing native species along Manali industrial perimeter as pollution buffer."},{"id":"CHE-WAT-001","name":"Pallikaranai Wetland Protection Order","category":"ecosystem","aqi_reduction_pct":4,"cost_inr_cr":0.5,"co2_reduction_tonnes":42,"implementation_days":7,"confidence":0.88,"score":6.84,"description":"Legal protection for Pallikaranai marshland to maintain natural air filtration function."}],"hotspots":[{"id":"CHE-001","name":"Manali Petrochemical Zone","type":"Industrial Zone","lat":13.166,"lon":80.258,"aqi":142,"pm25":78.4,"pm10":124.2,"no2":52.8,"co":1.8,"cluster":0,"is_anomaly":false,"anomaly_type":null},{"id":"CHE-002","name":"Ennore Port Entry Gate","type":"Port Terminal","lat":13.218,"lon":80.326,"aqi":124,"pm25":64.2,"pm10":98.6,"no2":44.1,"co":1.4,"cluster":0,"is_anomaly":false,"anomaly_type":null},{"id":"CHE-003","name":"Anna Nagar Residential","type":"Residential","lat":13.087,"lon":80.208,"aqi":72,"pm25":32.1,"pm10":58.4,"no2":24.2,"co":0.7,"cluster":-1,"is_anomaly":false,"anomaly_type":null},{"id":"CHE-004","name":"Marina Beach Promenade","type":"Coastal Park","lat":13.05,"lon":80.282,"aqi":44,"pm25":18.2,"pm10":34.1,"no2":14.2,"co":0.3,"cluster":-1,"is_anomaly":false,"anomaly_type":null}],"simulation_base":{"traffic":58,"industrial":42,"green":24,"wind":5.8,"rainfall":12,"base_aqi":120.0},"crisis_message":"Conditions are currently <strong>Satisfactory</strong>. XGBoost forecasts a gradual rise to <strong>128 AQI (Moderate)</strong> over 7 days. Proactive action recommended. Probability: <strong>28%</strong>."}'),
  hyderabad: JSON.parse('{"city_id":"hyderabad","city":"Hyderabad","zone":"Patancheru–Bollaram Chemical Corridor","lat":17.385,"lon":78.4867,"current_conditions":{"aqi":124,"pm25":64.8,"pm10":108.4,"no2":48.2,"so2":24.6,"co":1.2,"o3":47.9,"temperature":35.2,"humidity":42.0,"wind_speed":2.8,"rainfall":0.0,"ehi":29.8,"ehi_band":"Critical","status":"Moderate"},"forecast_summary":{"risk_probability":"74%","risk_classification":"Hazardous","max_forecast_aqi":214,"forecast":[{"day":"T+0","date":"Jun 05","aqi":124,"aqi_lower":108,"aqi_upper":140},{"day":"T+1","date":"Jun 06","aqi":138,"aqi_lower":120,"aqi_upper":156},{"day":"T+2","date":"Jun 07","aqi":151,"aqi_lower":132,"aqi_upper":170},{"day":"T+3","date":"Jun 08","aqi":162,"aqi_lower":141,"aqi_upper":183},{"day":"T+4","date":"Jun 09","aqi":178,"aqi_lower":155,"aqi_upper":201},{"day":"T+5","date":"Jun 10","aqi":194,"aqi_lower":169,"aqi_upper":219},{"day":"T+6","date":"Jun 11","aqi":214,"aqi_lower":186,"aqi_upper":242}]},"shap_values":{"base_value":78.4,"predicted_value":124.0,"contributions":[{"feature":"industrial_emissions","display_name":"Patancheru Chemical Emissions","feature_value":0.61,"shap_value":18.4},{"feature":"traffic_density","display_name":"Outer Ring Road Traffic","feature_value":0.68,"shap_value":14.2},{"feature":"heatwave_risk","display_name":"Heatwave Stress","feature_value":62.0,"shap_value":11.8},{"feature":"wind_speed","display_name":"Wind Stagnation","feature_value":2.8,"shap_value":8.2},{"feature":"vegetation_index","display_name":"Vegetation Cover","feature_value":0.16,"shap_value":5.6},{"feature":"pm10_lag1","display_name":"PM10 Lag (1-day)","feature_value":102.4,"shap_value":4.2},{"feature":"humidity","display_name":"Low Humidity","feature_value":42.0,"shap_value":-3.8}]},"interventions":[{"id":"HYD-IND-001","name":"Patancheru Chemical Plant Curtailment","category":"industrial","aqi_reduction_pct":20,"cost_inr_cr":3.2,"co2_reduction_tonnes":285,"implementation_days":2,"confidence":0.86,"score":9.02,"description":"Mandatory 20% production cut at Patancheru Special Economic Zone chemical units."},{"id":"HYD-TRF-001","name":"Outer Ring Road Freight Timing Control","category":"traffic","aqi_reduction_pct":13,"cost_inr_cr":0.3,"co2_reduction_tonnes":128,"implementation_days":1,"confidence":0.8,"score":8.14,"description":"Shift heavy freight to 10PM–5AM window on HMDA Outer Ring Road."},{"id":"HYD-WAT-001","name":"Hussain Sagar Lake Bioremediation","category":"ecosystem","aqi_reduction_pct":3,"cost_inr_cr":1.6,"co2_reduction_tonnes":28,"implementation_days":30,"confidence":0.61,"score":5.44,"description":"Accelerate bioremediation of Hussain Sagar to reduce methane and particulate release."},{"id":"HYD-GRN-001","name":"Bollaram Industrial Green Wall","category":"vegetation","aqi_reduction_pct":8,"cost_inr_cr":1.1,"co2_reduction_tonnes":62,"implementation_days":10,"confidence":0.7,"score":6.88,"description":"Install 8km green wall of native shrubs along Bollaram industrial zone perimeter."},{"id":"HYD-TRF-002","name":"MMTS Rail Incentive (Free Pass Scheme)","category":"traffic","aqi_reduction_pct":9,"cost_inr_cr":0.7,"co2_reduction_tonnes":88,"implementation_days":1,"confidence":0.73,"score":7.12,"description":"Issue free MMTS/Metro passes during high-pollution days to shift commuters off roads."}],"hotspots":[{"id":"HYD-001","name":"Patancheru Industrial Area","type":"Chemical Zone","lat":17.527,"lon":78.264,"aqi":187,"pm25":102.4,"pm10":164.2,"no2":68.4,"co":2.2,"cluster":0,"is_anomaly":false,"anomaly_type":null},{"id":"HYD-002","name":"Bollaram Industrial Estate","type":"Industrial Zone","lat":17.502,"lon":78.322,"aqi":168,"pm25":88.2,"pm10":142.6,"no2":58.1,"co":1.9,"cluster":0,"is_anomaly":false,"anomaly_type":null},{"id":"HYD-003","name":"Hitech City Madhapur","type":"IT Hub","lat":17.447,"lon":78.381,"aqi":118,"pm25":58.4,"pm10":94.2,"no2":42.1,"co":1.2,"cluster":-1,"is_anomaly":false,"anomaly_type":null},{"id":"HYD-004","name":"Banjara Hills Residential","type":"Residential","lat":17.415,"lon":78.449,"aqi":98,"pm25":44.2,"pm10":76.8,"no2":32.4,"co":0.8,"cluster":-1,"is_anomaly":false,"anomaly_type":null},{"id":"HYD-016","name":"ICRISAT Campus Monitor","type":"Research Campus","lat":17.532,"lon":78.274,"aqi":999,"pm25":0.0,"pm10":0.0,"no2":0.0,"co":0.0,"cluster":-1,"is_anomaly":true,"anomaly_type":"Firmware Error – Device requires recalibration"}],"simulation_base":{"traffic":68,"industrial":61,"green":16,"wind":2.8,"rainfall":0,"base_aqi":175.0},"crisis_message":"XGBoost projects AQI to cross <strong>200 (Hazardous)</strong> in <strong>7 days</strong>. Chemical corridor emissions are the primary driver. Exceedance Probability: <strong>74%</strong>."}')
};

// City meta for selector
const OFFLINE_CITY_LIST = [
  { id: "bengaluru", name: "Bengaluru", zone: "Peenya–Whitefield Industrial Corridor", aqi: 168, ehi: 23.0, ehi_band: "Critical", status: "Unhealthy", lat: 12.9716, lon: 77.5946, risk_probability: "91%", risk_classification: "Hazardous" },
  { id: "delhi", name: "Delhi NCR", zone: "Anand Vihar–Wazirpur Industrial Belt", aqi: 342, ehi: 8.2, ehi_band: "Emergency", status: "Severe", lat: 28.6139, lon: 77.2090, risk_probability: "98%", risk_classification: "Hazardous" },
  { id: "mumbai", name: "Mumbai", zone: "Dharavi–Chembur Industrial Harbor", aqi: 145, ehi: 34.2, ehi_band: "Critical", status: "Moderate", lat: 19.0760, lon: 72.8777, risk_probability: "62%", risk_classification: "High" },
  { id: "chennai", name: "Chennai", zone: "Manali–Ennore Industrial Port Cluster", aqi: 82, ehi: 48.6, ehi_band: "Stressed", status: "Satisfactory", lat: 13.0827, lon: 80.2707, risk_probability: "28%", risk_classification: "Moderate" },
  { id: "hyderabad", name: "Hyderabad", zone: "Patancheru–Bollaram Chemical Corridor", aqi: 124, ehi: 29.8, ehi_band: "Critical", status: "Moderate", lat: 17.3850, lon: 78.4867, risk_probability: "74%", risk_classification: "Hazardous" }
];

// NDVI zone config per city
const NDVI_ZONES = {
  bengaluru: [
    { id: "ZONE-A", name: "Bannerghatta Forest Loss", desc: "NDVI: 0.68 → 0.42 (-38.2%)", color: "#FF4444", coords: [[77.560, 12.780], [77.595, 12.780], [77.595, 12.815], [77.560, 12.815], [77.560, 12.780]] },
    { id: "ZONE-B", name: "Bellandur Lake Shrinkage", desc: "NDVI: 0.35 → 0.12 (-65.7%)", color: "#FFB800", coords: [[77.650, 12.920], [77.685, 12.920], [77.685, 12.945], [77.650, 12.945], [77.650, 12.920]] },
    { id: "ZONE-C", name: "Whitefield Urban Expansion", desc: "NDVI: 0.45 → 0.18 (-60.0%)", color: "#00D4FF", coords: [[77.730, 12.950], [77.770, 12.950], [77.770, 12.990], [77.730, 12.990], [77.730, 12.950]] }
  ],
  delhi: [
    { id: "ZONE-A", name: "Yamuna Floodplain Encroachment", desc: "NDVI: 0.52 → 0.28 (-46.2%)", color: "#FF4444", coords: [[77.200, 28.600], [77.240, 28.600], [77.240, 28.640], [77.200, 28.640], [77.200, 28.600]] },
    { id: "ZONE-B", name: "Okhla Wildlife Sanctuary Buffer", desc: "NDVI: 0.64 → 0.38 (-40.6%)", color: "#FFB800", coords: [[77.290, 28.550], [77.320, 28.550], [77.320, 28.580], [77.290, 28.580], [77.290, 28.550]] },
    { id: "ZONE-C", name: "Northern Ridge Forest Degradation", desc: "NDVI: 0.58 → 0.31 (-46.6%)", color: "#00D4FF", coords: [[77.140, 28.700], [77.180, 28.700], [77.180, 28.730], [77.140, 28.730], [77.140, 28.700]] }
  ],
  mumbai: [
    { id: "ZONE-A", name: "Thane Creek Mangrove Loss", desc: "NDVI: 0.72 → 0.44 (-38.9%)", color: "#FF4444", coords: [[72.920, 19.040], [72.960, 19.040], [72.960, 19.080], [72.920, 19.080], [72.920, 19.040]] },
    { id: "ZONE-B", name: "Aarey Colony Deforestation", desc: "NDVI: 0.68 → 0.42 (-38.2%)", color: "#FFB800", coords: [[72.856, 19.148], [72.890, 19.148], [72.890, 19.178], [72.856, 19.178], [72.856, 19.148]] },
    { id: "ZONE-C", name: "Dharavi Urban Greenery Loss", desc: "NDVI: 0.18 → 0.06 (-66.7%)", color: "#00D4FF", coords: [[72.840, 19.030], [72.870, 19.030], [72.870, 19.055], [72.840, 19.055], [72.840, 19.030]] }
  ],
  chennai: [
    { id: "ZONE-A", name: "Pallikaranai Wetland Shrinkage", desc: "NDVI: 0.61 → 0.32 (-47.5%)", color: "#FF4444", coords: [[80.218, 12.916], [80.252, 12.916], [80.252, 12.942], [80.218, 12.942], [80.218, 12.916]] },
    { id: "ZONE-B", name: "Ennore Port Coastal Erosion", desc: "NDVI: 0.45 → 0.19 (-57.8%)", color: "#FFB800", coords: [[80.300, 13.200], [80.340, 13.200], [80.340, 13.230], [80.300, 13.230], [80.300, 13.200]] },
    { id: "ZONE-C", name: "Poonamallee Farmland Loss", desc: "NDVI: 0.55 → 0.24 (-56.4%)", color: "#00D4FF", coords: [[80.075, 13.020], [80.110, 13.020], [80.110, 13.050], [80.075, 13.050], [80.075, 13.020]] }
  ],
  hyderabad: [
    { id: "ZONE-A", name: "Hussain Sagar Lake Decline", desc: "NDVI: 0.48 → 0.22 (-54.2%)", color: "#FF4444", coords: [[78.440, 17.410], [78.470, 17.410], [78.470, 17.440], [78.440, 17.440], [78.440, 17.410]] },
    { id: "ZONE-B", name: "Patancheru Industrial Encroachment", desc: "NDVI: 0.54 → 0.28 (-48.1%)", color: "#FFB800", coords: [[78.240, 17.510], [78.285, 17.510], [78.285, 17.545], [78.240, 17.545], [78.240, 17.510]] },
    { id: "ZONE-C", name: "Outer Ring Road Agricultural Loss", desc: "NDVI: 0.62 → 0.34 (-45.2%)", color: "#00D4FF", coords: [[78.350, 17.350], [78.390, 17.350], [78.390, 17.385], [78.350, 17.385], [78.350, 17.350]] }
  ]
};

// ─────────────────────────────────────────────────────────────────────────────
// GLOBAL STATE
// ─────────────────────────────────────────────────────────────────────────────
let appState = {
  activeCityId: 'bengaluru',
  cityData: null,
  activeInterventions: new Set(),
  map: null,
  mapLayers: { hotspots: null, ndvi: null, anomalies: null },
  charts: { forecast: null, shap: null, simulation: null },
  currentTwin: { traffic: 82, industrial: 74, green: 12, wind: 1.2, rainfall: 0 }
};

const COLORS = {
  cyan: '#00D4FF', emerald: '#00FF88', amber: '#FFB800',
  red: '#FF4444', purple: '#B82FF6', blue: '#2F80ED', gray: '#626C7A'
};

// ─────────────────────────────────────────────────────────────────────────────
// BOOT
// ─────────────────────────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  initLandingPage();
  initSliders();
  initCopilot();
});

// ─────────────────────────────────────────────────────────────────────────────
// 1. LANDING → CITY SELECTOR → DASHBOARD
// ─────────────────────────────────────────────────────────────────────────────
function initLandingPage() {
  const launchBtn = document.getElementById('launch-btn');
  launchBtn.addEventListener('click', () => showCitySelector());

  document.getElementById('back-to-landing-btn').addEventListener('click', () => {
    transition('city-selector', 'landing-page');
  });

  document.getElementById('change-city-btn').addEventListener('click', () => {
    transition('command-center', 'city-selector');
    populateCitySelector();
  });
}

function showCitySelector() {
  populateCitySelector();
  transition('landing-page', 'city-selector');
}

async function populateCitySelector() {
  const container = document.getElementById('city-cards-container');
  container.innerHTML = '<div class="loading-cities"><div class="spinner"></div><p>Loading city data...</p></div>';

  let cities = OFFLINE_CITY_LIST;
  try {
    const res = await fetch('/api/v1/cities');
    if (res.ok) {
      const data = await res.json();
      if (data.cities && data.cities.length > 0) cities = data.cities;
    }
  } catch (e) {
    console.warn('[City Selector] API unavailable, using offline data.');
  }

  container.innerHTML = '';
  cities.forEach(city => {
    const card = document.createElement('div');
    card.className = 'city-selector-card';
    card.id = `city-card-${city.id}`;

    const ehiClass = getEHIBandBadgeClass(city.ehi);
    const aqiClass = getAQIBadgeClass(city.aqi);
    const riskColor = city.risk_classification === 'Hazardous' ? '#FF4444' : city.risk_classification === 'High' ? '#FFB800' : '#00FF88';

    card.innerHTML = `
      <div class="csc-header">
        <div class="csc-city-name">
          <i data-lucide="map-pin"></i>
          <h3>${city.name}</h3>
        </div>
        <span class="badge ${ehiClass}">EHI: ${city.ehi}</span>
      </div>
      <p class="csc-zone">${city.zone}</p>
      <div class="csc-metrics">
        <div class="csc-metric">
          <span class="csc-m-lbl">Current AQI</span>
          <span class="csc-m-val badge ${aqiClass}">${city.aqi}</span>
        </div>
        <div class="csc-metric">
          <span class="csc-m-lbl">Status</span>
          <span class="csc-m-val">${city.status}</span>
        </div>
        <div class="csc-metric">
          <span class="csc-m-lbl">7-Day Risk</span>
          <span class="csc-m-val" style="color:${riskColor}">${city.risk_probability} ${city.risk_classification}</span>
        </div>
      </div>
      <button class="launch-city-btn" data-city="${city.id}">
        <span>Launch Command Center</span>
        <i data-lucide="arrow-right"></i>
      </button>
    `;

    card.querySelector('.launch-city-btn').addEventListener('click', async () => {
      await launchDashboard(city.id);
    });

    container.appendChild(card);
  });

  lucide.createIcons();
}

async function launchDashboard(cityId) {
  appState.activeCityId = cityId;
  appState.activeInterventions.clear();
  transition('city-selector', 'command-center');

  // Show loading state
  document.getElementById('topbar-city-name').textContent = 'Loading...';

  await loadCityData(cityId);
  renderDashboard();

  // Init or reinitialize map
  if (appState.map) {
    appState.map.remove();
    appState.map = null;
    appState.mapLayers = { hotspots: null, ndvi: null, anomalies: null };
  }
  setTimeout(() => {
    initLeafletMap();
    initNavigation();
  }, 300);
}

function transition(fromId, toId) {
  const fromEl = document.getElementById(fromId);
  const toEl = document.getElementById(toId);
  fromEl.style.opacity = '0';
  fromEl.style.transition = 'opacity 0.4s ease';
  setTimeout(() => {
    fromEl.classList.add('hidden');
    fromEl.style.opacity = '';
    toEl.classList.remove('hidden');
    toEl.style.opacity = '0';
    toEl.style.transition = 'opacity 0.4s ease';
    requestAnimationFrame(() => { toEl.style.opacity = '1'; });
    window.dispatchEvent(new Event('resize'));
  }, 400);
}

// ─────────────────────────────────────────────────────────────────────────────
// 2. DATA LOADING — API → Offline Fallback
// ─────────────────────────────────────────────────────────────────────────────
async function loadCityData(cityId) {
  // Try API first
  try {
    const res = await fetch(`/api/v1/city/${cityId}`);
    if (res.ok) {
      const data = await res.json();
      appState.cityData = data;
      console.log(`[EcoPulse] Loaded ${cityId} from API`);
      return;
    }
  } catch (e) {
    console.warn(`[EcoPulse] API unavailable for ${cityId}. Using offline fallback.`);
  }

  // Offline fallback
  if (OFFLINE_CITIES[cityId]) {
    appState.cityData = OFFLINE_CITIES[cityId];
    console.log(`[EcoPulse] Using offline data for ${cityId}`);
  } else {
    // For cities not in offline cache, load bengaluru with a note
    appState.cityData = { ...OFFLINE_CITIES.bengaluru, city_id: cityId };
    console.warn(`[EcoPulse] No offline data for ${cityId}, using bengaluru fallback`);
  }
}

// ─────────────────────────────────────────────────────────────────────────────
// 3. RENDER DASHBOARD
// ─────────────────────────────────────────────────────────────────────────────
function renderDashboard() {
  const data = appState.cityData;
  if (!data) return;

  const c = data.current_conditions;

  // Update header breadcrumb
  document.getElementById('topbar-city-name').textContent = data.city;
  document.getElementById('topbar-zone-name').textContent = data.zone;
  document.getElementById('sidebar-city-name').textContent = data.city;

  // Update crisis alert
  const crisisMsg = document.getElementById('crisis-message-text');
  if (data.crisis_message) {
    crisisMsg.innerHTML = data.crisis_message;
  }

  renderKPIs(data);
  renderPollutantPills(c);
  renderForecastChart(data.forecast_summary.forecast);
  renderSHAPChart(data.shap_values, c.aqi);
  renderInterventions(data.interventions);
  syncSliders(data.simulation_base);
  updateTwinOutputs();
  calculateCombinedImpact(data.interventions);
}

function renderKPIs(data) {
  const c = data.current_conditions;
  const ehi = c.ehi;
  const aqi = c.aqi;

  // EHI Gauge
  document.getElementById('ehi-value').innerText = Math.round(ehi);
  const offset = ((100 - ehi) / 100) * 251.2;
  document.getElementById('ehi-circle-fill').style.strokeDashoffset = offset;
  document.getElementById('ehi-band').innerText = getEHIBandText(ehi);
  document.getElementById('ehi-band').className = `badge ${getEHIBandBadgeClass(ehi)}`;

  // AQI Needle
  document.getElementById('current-aqi').innerText = aqi;
  const deg = (aqi / 500) * 180 - 90;
  document.getElementById('aqi-needle').style.transform = `rotate(${deg}deg)`;
  document.getElementById('aqi-status').innerText = getAQIStatusText(aqi);
  document.getElementById('aqi-status').className = `badge ${getAQIBadgeClass(aqi)}`;

  // Crisis Timeline
  const maxAqi = data.forecast_summary.max_forecast_aqi;
  if (maxAqi > 200) {
    document.getElementById('crisis-timeline-label').innerHTML = `<i data-lucide="shield-alert"></i> Hazardous threshold exceedance projected.`;
    document.getElementById('crisis-progress-bar').className = 'progress-bar-fill danger';
  } else {
    document.getElementById('crisis-timeline-label').innerHTML = `<i data-lucide="check-circle"></i> Conditions manageable. Monitor closely.`;
    document.getElementById('crisis-progress-bar').className = 'progress-bar-fill moderate';
  }

  // Hotspot / Anomaly counts
  const hotspots = data.hotspots || [];
  const clusters = new Set(hotspots.filter(s => !s.is_anomaly && s.cluster !== -1).map(s => s.cluster));
  const anomalies = hotspots.filter(s => s.is_anomaly).length;
  document.getElementById('active-hotspots').innerText = clusters.size;
  document.getElementById('sensor-anomalies').innerText = anomalies;

  lucide.createIcons();
}

function renderPollutantPills(c) {
  const setVal = (id, val) => {
    const el = document.getElementById(id);
    if (el && val !== undefined) el.innerText = val;
  };
  setVal('pill-pm25', c.pm25);
  setVal('pill-pm10', c.pm10);
  setVal('pill-no2', c.no2);
  setVal('pill-so2', c.so2);
  setVal('pill-co', c.co);
  setVal('pill-o3', c.o3);
  setVal('pill-temp', c.temperature);
  setVal('pill-wind', c.wind_speed);
  setVal('pill-humidity', c.humidity);
}

// ─────────────────────────────────────────────────────────────────────────────
// 4. NAVIGATION
// ─────────────────────────────────────────────────────────────────────────────
function initNavigation() {
  const navItems = document.querySelectorAll('.nav-item');
  navItems.forEach(item => {
    // Remove old listeners by cloning
    const clone = item.cloneNode(true);
    item.parentNode.replaceChild(clone, item);
  });

  document.querySelectorAll('.nav-item').forEach(item => {
    item.addEventListener('click', (e) => {
      e.preventDefault();
      document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
      item.classList.add('active');

      const tab = item.getAttribute('data-tab');
      let targetSel = null;

      if (tab === 'overview') {
        document.querySelector('.dashboard-content').scrollTo({ top: 0, behavior: 'smooth' });
        return;
      } else if (tab === 'geospatial' || tab === 'hotspots') {
        targetSel = '.map-card';
        if (tab === 'hotspots') toggleMapLayer('hotspots');
      } else if (tab === 'interventions') {
        targetSel = '#intervention-engine-section';
      } else if (tab === 'twin') {
        targetSel = '.digital-twin-card';
      }

      if (targetSel) {
        const el = document.querySelector(targetSel);
        if (el) {
          el.scrollIntoView({ behavior: 'smooth', block: 'center' });
          el.style.boxShadow = `0 0 24px ${COLORS.cyan}`;
          setTimeout(() => { el.style.boxShadow = ''; }, 1200);
        }
      }
    });
  });

  // Alert button
  const alertBtn = document.querySelector('.scroll-to-interventions');
  if (alertBtn) {
    alertBtn.addEventListener('click', () => {
      document.querySelector('#intervention-engine-section')?.scrollIntoView({ behavior: 'smooth', block: 'center' });
    });
  }
}

// ─────────────────────────────────────────────────────────────────────────────
// 5. FORECAST CHART
// ─────────────────────────────────────────────────────────────────────────────
function renderForecastChart(forecast) {
  const ctx = document.getElementById('forecastChart').getContext('2d');
  const labels = forecast.map(f => f.day);
  const median = forecast.map(f => f.aqi);
  const lower = forecast.map(f => f.aqi_lower);
  const upper = forecast.map(f => f.aqi_upper);

  if (appState.charts.forecast) appState.charts.forecast.destroy();

  const minY = Math.max(0, Math.min(...lower) - 20);
  const maxY = Math.min(500, Math.max(...upper) + 30);

  appState.charts.forecast = new Chart(ctx, {
    type: 'line',
    data: {
      labels,
      datasets: [
        {
          label: 'Median Projection', data: median,
          borderColor: COLORS.cyan, backgroundColor: 'transparent',
          borderWidth: 2.5, pointRadius: 4, pointHoverRadius: 6,
          pointBackgroundColor: COLORS.cyan, tension: 0.3, order: 1
        },
        {
          label: 'Lower Bound', data: lower,
          borderColor: 'transparent', backgroundColor: 'transparent',
          pointRadius: 0, fill: false, order: 3
        },
        {
          label: 'Upper Bound', data: upper,
          borderColor: 'transparent', backgroundColor: 'rgba(0, 212, 255, 0.08)',
          pointRadius: 0, fill: '-1', tension: 0.3, order: 2
        }
      ]
    },
    options: {
      responsive: true, maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          mode: 'index', intersect: false,
          backgroundColor: 'rgba(8,13,28,0.95)', titleColor: '#FFF', bodyColor: '#9FA6B2',
          borderColor: 'rgba(255,255,255,0.08)', borderWidth: 1,
          callbacks: {
            label(ctx) {
              if (ctx.datasetIndex === 0) return `Projected AQI: ${ctx.parsed.y}`;
              if (ctx.datasetIndex === 2) {
                const lo = ctx.chart.data.datasets[1].data[ctx.dataIndex];
                return `90% CI: [${lo} – ${ctx.parsed.y}]`;
              }
              return null;
            }
          }
        }
      },
      scales: {
        x: { grid: { color: 'rgba(255,255,255,0.03)' }, ticks: { color: '#626C7A', font: { family: 'Inter' } } },
        y: { grid: { color: 'rgba(255,255,255,0.03)' }, ticks: { color: '#626C7A', font: { family: 'Inter' } }, min: minY, max: maxY }
      }
    }
  });
}

// ─────────────────────────────────────────────────────────────────────────────
// 6. SHAP CHART
// ─────────────────────────────────────────────────────────────────────────────
function renderSHAPChart(shapData, aqi) {
  const ctx = document.getElementById('shapChart').getContext('2d');
  const subtitle = document.getElementById('shap-subtitle');
  if (subtitle) subtitle.textContent = `Feature contribution to current prediction (AQI: ${aqi})`;

  const contribs = (shapData.contributions || []).slice(0, 6);
  const labels = contribs.map(c => c.display_name);
  const values = contribs.map(c => c.shap_value);
  const barColors = values.map(v => v >= 0 ? COLORS.red : COLORS.emerald);

  if (appState.charts.shap) appState.charts.shap.destroy();

  appState.charts.shap = new Chart(ctx, {
    type: 'bar',
    data: { labels, datasets: [{ data: values, backgroundColor: barColors, borderRadius: 4, borderWidth: 0 }] },
    options: {
      indexAxis: 'y', responsive: true, maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: 'rgba(8,13,28,0.95)', titleColor: '#FFF', bodyColor: '#9FA6B2',
          callbacks: { label(ctx) { const s = ctx.parsed.x >= 0 ? '+' : ''; return `Impact: ${s}${ctx.parsed.x.toFixed(1)} AQI pts`; } }
        }
      },
      scales: {
        x: { grid: { color: 'rgba(255,255,255,0.03)' }, ticks: { color: '#626C7A' } },
        y: { grid: { display: false }, ticks: { color: '#FFFFFF', font: { weight: '600' } } }
      }
    }
  });

  const listEl = document.getElementById('shap-features-list');
  listEl.innerHTML = '';
  contribs.forEach(c => {
    const li = document.createElement('li');
    li.className = 'shap-item';
    const sign = c.shap_value >= 0 ? '+' : '';
    const colorClass = c.shap_value >= 0 ? 'positive' : 'negative';
    let valStr = c.feature_value;
    if (c.feature === 'industrial_emissions' || c.feature === 'traffic_density') valStr = `${Math.round(c.feature_value * 100)}%`;
    else if (c.feature === 'vegetation_index') valStr = `${Math.round(c.feature_value * 100)}% NDVI`;
    else if (c.feature === 'wind_speed') valStr = `${c.feature_value} m/s`;
    li.innerHTML = `<span class="shap-feat-name">${c.display_name} (${valStr})</span><span class="shap-feat-impact ${colorClass}">${sign}${c.shap_value.toFixed(1)}</span>`;
    listEl.appendChild(li);
  });
}

// ─────────────────────────────────────────────────────────────────────────────
// 7. INTERVENTION ENGINE
// ─────────────────────────────────────────────────────────────────────────────
function renderInterventions(interventions) {
  const container = document.getElementById('interventions-container');
  container.innerHTML = '';

  interventions.forEach(item => {
    const isActive = appState.activeInterventions.has(item.id);
    const card = document.createElement('div');
    card.className = `intervention-card-item ${isActive ? 'active' : ''}`;
    card.id = `int-card-${item.id}`;

    card.innerHTML = `
      <div class="int-left">
        <div class="int-title-row">
          <h5>${item.name}</h5>
          <span class="badge ${item.score > 8.5 ? 'badge-danger' : 'badge-warning'}">Score: ${item.score}</span>
        </div>
        <div class="int-metrics-row">
          <span class="int-metric-pill">AQI: -${item.aqi_reduction_pct}%</span>
          <span class="int-metric-pill">Cost: ₹${item.cost_inr_cr} Cr</span>
          <span class="int-metric-pill">Timeline: ${item.implementation_days}d</span>
        </div>
      </div>
      <div class="int-right">
        <div class="int-confidence-bar" title="Confidence: ${Math.round(item.confidence * 100)}%">
          <div class="int-confidence-fill" style="width: ${item.confidence * 100}%"></div>
        </div>
        <button class="apply-btn ${isActive ? 'active' : ''}" data-id="${item.id}">
          ${isActive ? 'Active ✓' : 'Apply'}
        </button>
      </div>
    `;

    const btn = card.querySelector('.apply-btn');
    btn.addEventListener('click', () => toggleIntervention(item.id, card, btn));
    container.appendChild(card);
  });

  calculateCombinedImpact(interventions);
}

function toggleIntervention(id, card, btn) {
  if (appState.activeInterventions.has(id)) {
    appState.activeInterventions.delete(id);
    card.classList.remove('active');
    btn.classList.remove('active');
    btn.innerText = 'Apply';
  } else {
    appState.activeInterventions.add(id);
    card.classList.add('active');
    btn.classList.add('active');
    btn.innerText = 'Active ✓';
    card.style.boxShadow = `0 0 12px ${COLORS.emerald}`;
    setTimeout(() => { card.style.boxShadow = ''; }, 800);
  }
  calculateCombinedImpact(appState.cityData.interventions);
}

function calculateCombinedImpact(interventions) {
  const selected = interventions.filter(i => appState.activeInterventions.has(i.id));
  const maxForecastAqi = appState.cityData?.forecast_summary?.max_forecast_aqi || 287;

  document.getElementById('old-proj-aqi').innerText = maxForecastAqi;

  if (selected.length === 0) {
    document.getElementById('new-proj-aqi').innerText = maxForecastAqi;
    document.getElementById('new-proj-aqi').className = 'new-aqi text-red';
    document.getElementById('combined-reduction').innerText = '0%';
    document.getElementById('combined-cost').innerText = '₹0 Cr';
    document.getElementById('combined-co2').innerText = '0 t';
    document.getElementById('combined-time').innerText = '0 Days';
    document.getElementById('impact-outcome-message').className = 'impact-outcome-box warning';
    document.getElementById('impact-outcome-message').innerHTML = `<i data-lucide="alert-triangle"></i><span><strong>No Action Taken:</strong> Select interventions above to simulate their combined impact.</span>`;
    lucide.createIcons();
    return;
  }

  // Diminishing returns
  let product = 1.0;
  selected.forEach(i => { product *= (1.0 - (i.aqi_reduction_pct / 100.0)); });
  const combinedReduction = roundNum((1.0 - product) * 100, 1);
  const totalCost = roundNum(selected.reduce((s, i) => s + i.cost_inr_cr, 0), 2);
  const totalCO2 = roundNum(selected.reduce((s, i) => s + i.co2_reduction_tonnes, 0), 0);
  const maxDays = Math.max(...selected.map(i => i.implementation_days));
  const newAqi = Math.round(maxForecastAqi * (1.0 - (combinedReduction / 100.0)));

  document.getElementById('new-proj-aqi').innerText = newAqi;
  document.getElementById('combined-reduction').innerText = `-${combinedReduction}%`;
  document.getElementById('combined-cost').innerText = `₹${totalCost} Cr`;
  document.getElementById('combined-co2').innerText = `${totalCO2} t`;
  document.getElementById('combined-time').innerText = `${maxDays} Days`;

  const outcomeBox = document.getElementById('impact-outcome-message');
  if (newAqi < 200) {
    document.getElementById('new-proj-aqi').className = 'new-aqi text-emerald';
    outcomeBox.className = 'impact-outcome-box averted';
    outcomeBox.innerHTML = `<i data-lucide="shield-check"></i><span><strong>Hazardous Event Averted:</strong> Top interventions reduce projected AQI to ${newAqi}. Residents protected from critical exposure.</span>`;
  } else {
    document.getElementById('new-proj-aqi').className = 'new-aqi text-warning';
    outcomeBox.className = 'impact-outcome-box warning';
    outcomeBox.innerHTML = `<i data-lucide="alert-circle"></i><span><strong>Insufficient Intervention:</strong> Projected AQI remains elevated at ${newAqi}. Additional actions required.</span>`;
  }
  lucide.createIcons();
}

// ─────────────────────────────────────────────────────────────────────────────
// 8. LEAFLET MAP
// ─────────────────────────────────────────────────────────────────────────────
function initLeafletMap() {
  if (appState.map) return;

  const data = appState.cityData;
  const lat = data?.lat || 12.9716;
  const lon = data?.lon || 77.5946;

  appState.map = L.map('map', { zoomControl: false, attributionControl: false }).setView([lat, lon], 11);
  L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', { maxZoom: 19 }).addTo(appState.map);

  appState.mapLayers.hotspots = L.layerGroup().addTo(appState.map);
  appState.mapLayers.anomalies = L.layerGroup().addTo(appState.map);
  appState.mapLayers.ndvi = L.layerGroup();

  updateMapOverlays();
  updateNDVIPanel();

  document.getElementById('btn-toggle-hotspots').addEventListener('click', (e) => toggleMapLayer('hotspots', e.target));
  document.getElementById('btn-toggle-ndvi').addEventListener('click', (e) => toggleMapLayer('ndvi', e.target));
  document.getElementById('btn-toggle-anomalies').addEventListener('click', (e) => toggleMapLayer('anomalies', e.target));

  document.querySelectorAll('.ndvi-zone-item').forEach(item => {
    item.addEventListener('click', () => {
      document.querySelectorAll('.ndvi-zone-item').forEach(i => i.classList.remove('active'));
      item.classList.add('active');
      highlightNDVIZone(item.getAttribute('data-zone'));
    });
  });
}

function updateMapOverlays() {
  const data = appState.cityData;
  if (!data || !appState.map) return;

  appState.mapLayers.hotspots.clearLayers();
  appState.mapLayers.anomalies.clearLayers();
  appState.mapLayers.ndvi.clearLayers();

  (data.hotspots || []).forEach(station => {
    const coords = [station.lat, station.lon];

    if (station.is_anomaly) {
      const icon = L.divIcon({
        className: '',
        html: `<div style="background:${COLORS.amber};width:12px;height:12px;border-radius:50%;border:2px solid white;box-shadow:0 0 8px ${COLORS.amber}"></div>`,
        iconSize: [12, 12]
      });
      const marker = L.marker(coords, { icon });
      marker.bindPopup(`
        <div class="map-popup-card">
          <h4 style="color:#FFB800">DATA INTEGRITY ALERT</h4>
          <p><strong>${station.name}</strong> (${station.type})</p>
          <p>Status: <span style="color:#FFB800">Anomaly Flagged</span></p>
          <p>Reason: <strong>${station.anomaly_type}</strong></p>
          <div class="map-popup-grid">
            <div class="mpg-item"><span class="mpg-lbl">Reported AQI</span><span class="mpg-val">${station.aqi}</span></div>
          </div>
        </div>
      `);
      appState.mapLayers.anomalies.addLayer(marker);
    } else {
      let color = COLORS.emerald;
      if (station.cluster === 0) color = COLORS.red;
      else if (station.cluster === 1) color = COLORS.purple;
      else if (station.aqi > 150) color = COLORS.amber;

      const circle = L.circleMarker(coords, {
        radius: station.cluster !== -1 ? 10 : 7,
        fillColor: color, color: '#FFF', weight: 1, fillOpacity: 0.8
      });

      let clusterLabel = 'Isolated Station';
      if (station.cluster === 0) clusterLabel = 'Hotspot Cluster 1 (Primary)';
      if (station.cluster === 1) clusterLabel = 'Hotspot Cluster 2 (Secondary)';

      circle.bindPopup(`
        <div class="map-popup-card">
          <h4>${clusterLabel}</h4>
          <p><strong>${station.name}</strong> (${station.type})</p>
          <p>AQI: <strong style="color:${station.aqi > 200 ? '#FF4444' : station.aqi > 150 ? '#FFB800' : '#00FF88'}">${station.aqi}</strong></p>
          <div class="map-popup-grid">
            <div class="mpg-item"><span class="mpg-lbl">PM2.5</span><span class="mpg-val">${station.pm25} μg/m³</span></div>
            <div class="mpg-item"><span class="mpg-lbl">PM10</span><span class="mpg-val">${station.pm10} μg/m³</span></div>
            <div class="mpg-item"><span class="mpg-lbl">NO₂</span><span class="mpg-val">${station.no2} μg/m³</span></div>
            <div class="mpg-item"><span class="mpg-lbl">CO</span><span class="mpg-val">${station.co} ppm</span></div>
          </div>
        </div>
      `);
      appState.mapLayers.hotspots.addLayer(circle);
    }
  });

  // Draw NDVI zones
  const cityId = appState.activeCityId;
  const zones = NDVI_ZONES[cityId] || NDVI_ZONES.bengaluru;
  zones.forEach(zone => {
    const polygon = L.polygon([zone.coords.map(c => [c[1], c[0]])], {
      fillColor: zone.color, color: zone.color, weight: 1, fillOpacity: 0.2
    });
    polygon.options.id = zone.id;
    polygon.options.baseColor = zone.color;
    polygon.bindPopup(`<strong>${zone.name}</strong><br>${zone.desc}`);
    appState.mapLayers.ndvi.addLayer(polygon);
  });
}

function updateNDVIPanel() {
  const cityId = appState.activeCityId;
  const zones = NDVI_ZONES[cityId] || NDVI_ZONES.bengaluru;
  const ids = ['ZONE-A', 'ZONE-B', 'ZONE-C'];
  ids.forEach((zid, i) => {
    const zone = zones.find(z => z.id === zid);
    const descEl = document.getElementById(`ndvi-zone-${zid.toLowerCase().replace('zone-', 'zone-')}-desc`) ||
      document.querySelectorAll('.ndvi-zone-item')[i]?.querySelector('p');
    if (descEl && zone) descEl.textContent = zone.desc;
    const nameEl = document.querySelectorAll('.ndvi-zone-item')[i]?.querySelector('h5');
    if (nameEl && zone) nameEl.textContent = zone.name;
  });
}

function toggleMapLayer(layerName, buttonEl = null) {
  if (!appState.map) return;
  const layer = appState.mapLayers[layerName];
  const ndviPanel = document.getElementById('ndvi-selector-panel');
  if (buttonEl) buttonEl.classList.toggle('active');
  if (appState.map.hasLayer(layer)) {
    appState.map.removeLayer(layer);
    if (layerName === 'ndvi') ndviPanel.classList.add('hidden');
  } else {
    appState.map.addLayer(layer);
    if (layerName === 'ndvi') { ndviPanel.classList.remove('hidden'); highlightNDVIZone('ZONE-A'); }
  }
}

function highlightNDVIZone(zoneId) {
  appState.mapLayers.ndvi.eachLayer(layer => {
    if (layer.options.id === zoneId) {
      layer.setStyle({ fillOpacity: 0.5, weight: 3, color: COLORS.cyan });
      appState.map.fitBounds(layer.getBounds(), { padding: [30, 30] });
    } else {
      layer.setStyle({ fillOpacity: 0.2, weight: 1, color: layer.options.baseColor });
    }
  });
}

// ─────────────────────────────────────────────────────────────────────────────
// 9. DIGITAL TWIN SLIDERS
// ─────────────────────────────────────────────────────────────────────────────
function syncSliders(base) {
  if (!base) return;
  const map = { traffic: base.traffic, industrial: base.industrial, green: base.green, wind: base.wind, rainfall: base.rainfall };
  Object.entries(map).forEach(([key, val]) => {
    const slider = document.getElementById(`slider-${key}`);
    const display = document.getElementById(`val-${key}`);
    if (slider) slider.value = val;
    if (display) display.innerText = formatSliderVal(key, val);
    appState.currentTwin[key] = val;
  });
}

function formatSliderVal(key, val) {
  if (key === 'wind') return `${val} m/s`;
  if (key === 'rainfall') return `${val} mm`;
  return `${val}%`;
}

function initSliders() {
  ['traffic', 'industrial', 'green', 'wind', 'rainfall'].forEach(s => {
    const slider = document.getElementById(`slider-${s}`);
    const display = document.getElementById(`val-${s}`);
    if (!slider) return;
    slider.addEventListener('input', () => {
      display.innerText = formatSliderVal(s, slider.value);
      appState.currentTwin[s] = parseFloat(slider.value);
      updateTwinOutputs();
    });
  });

  document.getElementById('reset-sliders-btn')?.addEventListener('click', () => {
    const base = appState.cityData?.simulation_base || { traffic: 82, industrial: 74, green: 12, wind: 1.2, rainfall: 0 };
    syncSliders(base);
    updateTwinOutputs();
  });
}

function updateTwinOutputs() {
  const twin = appState.currentTwin;
  const base_aqi = appState.cityData?.simulation_base?.base_aqi || 203.2;

  let sim_aqi = base_aqi + (twin.traffic * 0.8) + (twin.industrial * 1.2) - (twin.green * 15.0) - (twin.wind * 8.0) - (twin.rainfall * 0.3);
  sim_aqi = Math.max(0, Math.min(500, sim_aqi));

  let carbon = (twin.traffic * 4.2 + twin.industrial * 8.5) * (1.0 - (twin.green / 100.0));
  carbon = Math.max(0, roundNum(carbon, 1));

  const water_stress = Math.max(0, Math.min(100, 30.0 + (twin.industrial * 0.5) - (twin.rainfall * 0.2)));
  const heatwave_risk = Math.max(0, Math.min(100, 45.0 - (twin.green * 0.8) + (twin.industrial * 0.36)));
  const veg_loss = Math.max(0, Math.min(100, 100.0 - twin.green));

  const aqi_score = Math.max(0, 100.0 - (sim_aqi / 200.0) * 100.0);
  const ehi = roundNum((aqi_score * 0.40) + ((100 - water_stress) * 0.20) + ((100 - heatwave_risk) * 0.20) + ((100 - veg_loss) * 0.20), 1);

  let pop = 0;
  if (sim_aqi > 100) pop = Math.round((sim_aqi - 100) * 230);
  if (sim_aqi > 200) pop = Math.round(25000 + (sim_aqi - 200) * 207);

  const baseAqi = appState.cityData?.current_conditions?.aqi || 168;
  const baseEhi = appState.cityData?.current_conditions?.ehi || 23;

  document.getElementById('sim-aqi-val').innerText = Math.round(sim_aqi);
  document.getElementById('sim-aqi-val').className = `soc-val ${sim_aqi > 200 ? 'text-red' : sim_aqi > 150 ? 'text-amber' : 'text-emerald'}`;
  document.getElementById('sim-aqi-status').innerText = getAQIStatusText(sim_aqi);
  document.getElementById('sim-aqi-status').className = `badge ${getAQIBadgeClass(sim_aqi)}`;
  document.getElementById('sim-carbon-val').innerText = `${carbon} t`;
  document.getElementById('sim-ehi-val').innerText = ehi.toFixed(1);
  document.getElementById('sim-ehi-status').innerText = getEHIBandText(ehi);
  document.getElementById('sim-ehi-status').className = `badge ${getEHIBandBadgeClass(ehi)}`;
  document.getElementById('sim-pop-val').innerText = pop.toLocaleString('en-IN');

  renderSimulationChart(baseAqi, Math.round(sim_aqi), baseEhi, ehi);
}

function renderSimulationChart(beforeAqi, afterAqi, beforeEHI, afterEHI) {
  const ctx = document.getElementById('simulationChart').getContext('2d');
  if (appState.charts.simulation) appState.charts.simulation.destroy();

  appState.charts.simulation = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: ['AQI (Lower = Better)', 'EHI Score (Higher = Better)'],
      datasets: [
        { label: 'Current', data: [beforeAqi, beforeEHI], backgroundColor: '#B82FF6', borderRadius: 4 },
        { label: 'Simulated Twin', data: [afterAqi, afterEHI], backgroundColor: COLORS.cyan, borderRadius: 4 }
      ]
    },
    options: {
      responsive: true, maintainAspectRatio: false,
      plugins: {
        legend: { display: true, position: 'top', labels: { color: '#9FA6B2', font: { family: 'Inter', size: 10 } } }
      },
      scales: {
        x: { grid: { display: false }, ticks: { color: '#FFFFFF', font: { weight: '600' } } },
        y: { grid: { color: 'rgba(255,255,255,0.03)' }, ticks: { color: '#626C7A' }, max: 350 }
      }
    }
  });
}

// ─────────────────────────────────────────────────────────────────────────────
// 10. COPILOT CHAT
// ─────────────────────────────────────────────────────────────────────────────
function initCopilot() {
  document.getElementById('copilot-toggle-btn')?.addEventListener('click', () => {
    document.getElementById('copilot-sidebar').classList.toggle('hidden');
    document.getElementById('copilot-input')?.focus();
  });
  document.getElementById('close-copilot-btn')?.addEventListener('click', () => {
    document.getElementById('copilot-sidebar').classList.add('hidden');
  });
  document.getElementById('send-copilot-btn')?.addEventListener('click', sendCopilotMessage);
  document.getElementById('copilot-input')?.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendCopilotMessage();
  });
  document.querySelectorAll('.preset-btn-chat').forEach(p => {
    p.addEventListener('click', () => {
      document.getElementById('copilot-input').value = p.innerText;
      sendCopilotMessage();
    });
  });
}

async function sendCopilotMessage() {
  const input = document.getElementById('copilot-input');
  const query = input?.value.trim();
  if (!query) return;
  appendMessage(query, 'user');
  input.value = '';
  const typing = appendTypingIndicator();

  const context = {
    city: appState.cityData?.city || 'Unknown',
    current_aqi: appState.cityData?.current_conditions?.aqi,
    current_ehi: appState.cityData?.current_conditions?.ehi,
    active_interventions: Array.from(appState.activeInterventions)
  };

  try {
    const res = await fetch('/api/v1/copilot', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query, city_id: appState.activeCityId, context })
    });
    const data = await res.json();
    typing.remove();
    appendMessage(data.answer, 'bot', data.source);
  } catch (e) {
    typing.remove();
    appendMessage('Network issue. The local XGBoost models and Digital Twin sliders remain fully active offline.', 'bot', 'Local Edge AI Engine (Offline Fallback)');
  }
}

function appendMessage(text, sender, source = '') {
  const msgs = document.getElementById('chat-messages');
  const bubble = document.createElement('div');
  bubble.className = `chat-bubble ${sender}`;
  bubble.innerHTML = `<p>${text.replace(/\n/g, '<br/>')}</p>`;
  if (source) bubble.innerHTML += `<span class="source-cite">Source: ${source}</span>`;
  msgs.appendChild(bubble);
  msgs.scrollTop = msgs.scrollHeight;
  return bubble;
}

function appendTypingIndicator() {
  const msgs = document.getElementById('chat-messages');
  const bubble = document.createElement('div');
  bubble.className = 'chat-bubble bot typing-indicator-bubble';
  bubble.innerHTML = `<div class="typing-dots"><span></span><span></span><span></span></div>`;
  msgs.appendChild(bubble);
  msgs.scrollTop = msgs.scrollHeight;
  return bubble;
}

// ─────────────────────────────────────────────────────────────────────────────
// HELPERS
// ─────────────────────────────────────────────────────────────────────────────
function roundNum(value, decimals) {
  return Number(Math.round(Number(value + 'e' + decimals)) + 'e-' + decimals);
}

function getEHIBandText(ehi) {
  if (ehi < 20) return 'EMERGENCY';
  if (ehi < 40) return 'CRITICAL';
  if (ehi < 60) return 'STRESSED';
  if (ehi < 80) return 'MODERATE';
  return 'HEALTHY';
}

function getEHIBandBadgeClass(ehi) {
  if (ehi < 40) return 'badge-danger';
  if (ehi < 60) return 'badge-warning';
  if (ehi < 80) return 'badge-live';
  return 'badge-success';
}

function getAQIStatusText(aqi) {
  if (aqi <= 50) return 'GOOD';
  if (aqi <= 100) return 'SATISFACTORY';
  if (aqi <= 200) return 'UNHEALTHY';
  if (aqi <= 300) return 'POOR';
  if (aqi <= 400) return 'VERY POOR';
  return 'SEVERE';
}

function getAQIBadgeClass(aqi) {
  if (aqi <= 50) return 'badge-success';
  if (aqi <= 100) return 'badge-live';
  if (aqi <= 200) return 'badge-warning';
  return 'badge-danger';
}
