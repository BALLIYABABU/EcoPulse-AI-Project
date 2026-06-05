from demo_data import get_city, list_cities, CITIES

cities = list_cities()
print(f"Cities loaded: {len(cities)}")
for c in cities:
    print(f"  {c['name']}: AQI={c['aqi']}, EHI={c['ehi']}, Band={c['ehi_band']}, Risk={c['risk_probability']} {c['risk_classification']}")

print("\nBengaluru forecast (7 days):")
bng = get_city("bengaluru")
for f in bng["forecast"]:
    print(f"  {f['day']} ({f['date']}): AQI={f['aqi']} [{f['aqi_lower']}–{f['aqi_upper']}]")

print("\nInterventions (Delhi):")
delhi = get_city("delhi")
for iv in delhi["interventions"]:
    print(f"  {iv['id']}: {iv['name']} | Score={iv['score']}")

print("\nHotspots (Hyderabad):")
hyd = get_city("hyderabad")
for hs in hyd["hotspots"]:
    flag = "ANOMALY" if hs["is_anomaly"] else f"cluster={hs['cluster']}"
    print(f"  {hs['id']}: {hs['name']} | AQI={hs['aqi']} | {flag}")

print("\nAll checks passed!")
