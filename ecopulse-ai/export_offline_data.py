#!/usr/bin/env python
from demo_data import CITIES
import json

for city_id, city_data in CITIES.items():
    if city_id != 'bengaluru':  # We already have bengaluru
        c = city_data['current']
        offline = {
            'city_id': city_id,
            'city': city_data['name'],
            'zone': city_data['zone'],
            'lat': city_data['lat'],
            'lon': city_data['lon'],
            'current_conditions': {
                'aqi': c['aqi'],
                'pm25': c['pm25'],
                'pm10': c['pm10'],
                'no2': c['no2'],
                'so2': c['so2'],
                'co': c['co'],
                'o3': c['o3'],
                'temperature': c['temperature'],
                'humidity': c['humidity'],
                'wind_speed': c['wind_speed'],
                'rainfall': c['rainfall'],
                'ehi': c['ehi'],
                'ehi_band': c['ehi_band'],
                'status': c['status']
            },
            'forecast_summary': {
                'risk_probability': city_data['risk_probability'],
                'risk_classification': city_data['risk_classification'],
                'max_forecast_aqi': city_data['max_forecast_aqi'],
                'forecast': city_data['forecast']
            },
            'shap_values': city_data['shap_values'],
            'interventions': city_data['interventions'],
            'hotspots': city_data['hotspots'],
            'simulation_base': city_data['simulation_base'],
            'crisis_message': city_data['crisis_message']
        }
        print(f"  {city_id}: {json.dumps(offline, separators=(',', ':'))},")
