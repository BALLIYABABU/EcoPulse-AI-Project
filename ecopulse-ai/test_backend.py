import unittest
import os
import json
import asyncio
from fastapi.testclient import TestClient

# Import local modules
from ml_engine import MLEngine
from intervention_engine import InterventionEngine
from data_manager import DataManager
from main import app

class TestEcoPulseBackend(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ml_engine = MLEngine()
        cls.intervention_engine = InterventionEngine()
        cls.data_manager = DataManager()
        cls.client = TestClient(app)

    def test_data_manager_fallback(self):
        """Test the API fallback chain returns offline demo state when requested."""
        # Use asyncio to run the async method
        loop = asyncio.get_event_loop()
        state = loop.run_until_complete(self.data_manager.get_current_state("Bengaluru", live_mode=False))
        
        self.assertIn("aqi", state)
        self.assertEqual(state["aqi"], 168)
        self.assertEqual(state["industrial_emissions"], 0.74)
        self.assertEqual(state["traffic_density"], 0.82)
        self.assertIn("source", state)

    def test_ml_engine_forecaster(self):
        """Test that the 7-day recursive forecast returns 7 days of predictions."""
        forecast = self.ml_engine.forecast_7days()
        self.assertEqual(len(forecast), 7)
        for day in forecast:
            self.assertIn("day", day)
            self.assertIn("aqi", day)
            self.assertIn("aqi_lower", day)
            self.assertIn("aqi_upper", day)
            self.assertTrue(day["aqi_lower"] <= day["aqi"] <= day["aqi_upper"])

        # Test modifiers drop forecast (mitigation simulation)
        mitigated_forecast = self.ml_engine.forecast_7days(industrial_modifier=-0.15, traffic_modifier=-0.15)
        self.assertEqual(len(mitigated_forecast), 7)
        # Verify the mitigated AQI at T+7 is lower than base T+7
        self.assertLess(mitigated_forecast[6]["aqi"], forecast[6]["aqi"])

    def test_ml_engine_shap(self):
        """Test SHAP values are extracted and formatted properly."""
        shap_explanation = self.ml_engine.get_shap_explanation()
        self.assertIn("base_value", shap_explanation)
        self.assertIn("prediction", shap_explanation)
        self.assertIn("contributions", shap_explanation)
        
        contribs = shap_explanation["contributions"]
        self.assertGreater(len(contribs), 0)
        
        # Verify it has display name and value
        first_contrib = contribs[0]
        self.assertIn("display_name", first_contrib)
        self.assertIn("shap_value", first_contrib)
        self.assertIn("feature_value", first_contrib)

    def test_ml_engine_hotspots_and_anomalies(self):
        """Test DBSCAN and Isolation Forest group hotspots and detect anomalies."""
        stations = self.ml_engine.cluster_hotspots()
        self.assertGreater(len(stations), 0)
        
        # Verify anomalous stations are flagged
        anomalies = [s for s in stations if s["is_anomaly"]]
        self.assertGreaterEqual(len(anomalies), 2)
        
        names = [s["name"] for s in anomalies]
        self.assertTrue(any("Silk Board" in n for n in names))
        self.assertTrue(any("ORR Station" in n for n in names))

        # Verify cluster groups exist
        clusters = [s["cluster"] for s in stations if s["cluster"] != -1]
        self.assertGreater(len(set(clusters)), 0)

    def test_intervention_scoring(self):
        """Test that scoring ranks interventions properly."""
        context = {
            "industrial_emissions": 0.74,
            "traffic_density": 0.82,
            "vegetation_index": 0.12,
            "pm25": 92.4,
            "pm10": 218.4,
            "humidity": 55.0,
            "wind_speed": 1.2
        }
        ranked = self.intervention_engine.rank_interventions(context)
        self.assertGreater(len(ranked), 0)
        # Check sorted descending
        for i in range(len(ranked) - 1):
            self.assertGreaterEqual(ranked[i]["score"], ranked[i+1]["score"])

    def test_combined_impact(self):
        """Test the diminishing returns simulation for multiple interventions."""
        # IND-001 (22% reduction), TRF-001 (18% reduction)
        selected_ids = ["IND-001", "TRF-001"]
        impact = self.intervention_engine.simulate_combined_impact(selected_ids)
        
        # Combined reduction = 1 - (1-0.22)*(1-0.18) = 1 - 0.78 * 0.82 = 1 - 0.6396 = 36.04%
        self.assertAlmostEqual(impact["aqi_reduction_pct"], 36.0, places=1)
        self.assertEqual(impact["cost_inr_cr"], 2.5) # 2.1 + 0.4
        self.assertEqual(impact["co2_reduction_tonnes"], 520) # 340 + 180
        self.assertEqual(impact["days_max"], 3) # max(3, 1)

    def test_fastapi_endpoints(self):
        """Test API endpoints respond successfully and quickly."""
        # 1. Health
        response = self.client.get("/api/v1/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "healthy")

        # 2. Demo
        response = self.client.get("/api/v1/demo")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["city"], "Bengaluru Industrial Corridor")
        self.assertEqual(data["current_conditions"]["aqi"], 168)

        # 3. Simulate
        payload = {
            "traffic_index": 82,
            "industrial_index": 74,
            "green_cover": 12,
            "wind_speed": 1.2,
            "rainfall": 0
        }
        response = self.client.post("/api/v1/simulate", json=payload)
        self.assertEqual(response.status_code, 200)
        sim_data = response.json()
        self.assertEqual(sim_data["simulated_aqi"], 168)
        self.assertEqual(sim_data["ehi"], 23.0)

        # 4. Copilot (Fallback check)
        payload_chat = {
            "query": "Why is pollution increasing in Bengaluru?",
            "context": {}
        }
        response = self.client.post("/api/v1/copilot", json=payload_chat)
        self.assertEqual(response.status_code, 200)
        self.assertIn("answer", response.json())
        self.assertIn("Local Edge", response.json()["source"])

if __name__ == "__main__":
    unittest.main()
