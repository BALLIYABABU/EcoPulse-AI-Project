import urllib.request
import json

def get(url):
    with urllib.request.urlopen(url) as r:
        return json.loads(r.read())

base = 'http://localhost:8000'

print("=== EcoPulse AI API Tests ===\n")

# 1. Health check
h = get(base + '/api/v1/health')
print("Health:", h)

# 2. Cities list
c = get(base + '/api/v1/cities')
print("\nCities API:", len(c['cities']), "cities loaded")
for city in c['cities']:
    print("  -", city['name'], "| AQI:", city['aqi'], "| EHI:", city['ehi'], "| Risk:", city['risk_probability'])

# 3. Full dashboard for each city
print("\nDashboard endpoints:")
for city_id in ['bengaluru', 'delhi', 'mumbai', 'chennai', 'hyderabad']:
    d = get(base + '/api/v1/city/' + city_id)
    cc = d['current_conditions']
    print("  [%s] AQI=%d, EHI=%.1f (%s), Interventions=%d, Hotspots=%d" % (
        city_id, cc['aqi'], cc['ehi'], cc['ehi_band'],
        len(d['interventions']), len(d['hotspots'])
    ))

# 4. Forecast endpoint
f = get(base + '/api/v1/forecast/bengaluru')
print("\nForecast (Bengaluru):", len(f['forecast']), "days | Max AQI:", f['max_forecast_aqi'], "| Risk:", f['risk_probability'])

# 5. SHAP endpoint
s = get(base + '/api/v1/shap/delhi')
print("SHAP (Delhi): base_value=%.1f, contributions=%d" % (s['base_value'], len(s['contributions'])))

# 6. Interventions endpoint
iv = get(base + '/api/v1/interventions/hyderabad')
print("Interventions (Hyderabad):", len(iv), "actions | Top:", iv[0]['name'])

# 7. Hotspots endpoint
hs = get(base + '/api/v1/hotspots/mumbai')
print("Hotspots (Mumbai):", len(hs), "stations |", len([h for h in hs if h['is_anomaly']]), "anomalies")

# 8. Simulation endpoint
import urllib.parse
sim_data = json.dumps({
    "city_id": "bengaluru",
    "traffic_index": 50,
    "industrial_index": 40,
    "green_cover": 30,
    "wind_speed": 8.0,
    "rainfall": 10
}).encode()
req = urllib.request.Request(base + '/api/v1/simulate',
    data=sim_data, headers={'Content-Type': 'application/json'})
with urllib.request.urlopen(req) as r:
    sim = json.loads(r.read())
print("Simulation: AQI=%d, EHI=%.1f, Pop@Risk=%s" % (sim['simulated_aqi'], sim['ehi'], sim['population_at_risk']))

# 9. Legacy demo endpoint
demo = get(base + '/api/v1/demo')
print("Legacy /demo: city=%s, interventions=%d" % (demo['city'], len(demo['interventions'])))

print("\n=== ALL API TESTS PASSED ===")
