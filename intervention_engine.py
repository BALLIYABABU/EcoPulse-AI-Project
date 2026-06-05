import json
import os

class InterventionEngine:
    def __init__(self, library_path="data/intervention_library.json"):
        self.library_path = library_path
        self.interventions = []
        self.load_library()

    def load_library(self):
        if os.path.exists(self.library_path):
            with open(self.library_path, "r") as f:
                self.interventions = json.load(f)

    def evaluate_condition(self, condition_str, context):
        """
        Evaluates a condition string against the context dictionary.
        Example condition: "industrial_emissions > 0.6"
        """
        try:
            # Simple token parsing: "key operator value"
            tokens = condition_str.split()
            if len(tokens) != 3:
                return False
                
            key, op, val_str = tokens
            val = float(val_str)
            
            if key not in context:
                return False
                
            context_val = float(context[key])
            
            if op == ">":
                return context_val > val
            elif op == "<":
                return context_val < val
            elif op == ">=":
                return context_val >= val
            elif op == "<=":
                return context_val <= val
            elif op == "==":
                return context_val == val
                
            return False
        except Exception:
            return False

    def get_applicable_interventions(self, context):
        """
        Filter interventions that meet the 'applicable_when' criteria.
        """
        applicable = []
        for item in self.interventions:
            rules = item.get("applicable_when", [])
            # If no rules, it's always applicable
            if not rules:
                applicable.append(item)
                continue
                
            # All rules must match
            match = True
            for rule in rules:
                if not self.evaluate_condition(rule, context):
                    match = False
                    break
            if match:
                applicable.append(item)
        return applicable

    def score_intervention(self, intervention):
        """
        intervention_score = aqi_reduction_pct * 0.40
                           + confidence * 0.30
                           + (1 / cost_inr_cr) * 0.20
                           + (1 / implementation_days) * 0.10
        """
        reduction = float(intervention.get("aqi_reduction_pct", 0))
        confidence = float(intervention.get("confidence", 0.5))
        cost = float(intervention.get("cost_inr_cr", 1.0))
        days = float(intervention.get("implementation_days", 1.0))
        
        # Avoid division by zero
        cost_term = 1.0 / cost if cost > 0 else 0
        days_term = 1.0 / days if days > 0 else 0
        
        score = (
            reduction * 0.40 +
            confidence * 0.30 +
            cost_term * 0.20 +
            days_term * 0.10
        )
        return round(score, 3)

    def rank_interventions(self, context):
        """
        Get applicable interventions, score them, and rank in descending order.
        """
        applicable = self.get_applicable_interventions(context)
        ranked = []
        for item in applicable:
            scored_item = item.copy()
            scored_item["score"] = self.score_intervention(item)
            ranked.append(scored_item)
            
        # Sort by score descending
        ranked = sorted(ranked, key=lambda x: x["score"], reverse=True)
        return ranked

    def simulate_combined_impact(self, selected_ids):
        """
        Simulate combined reduction using a diminishing returns model:
        combined_reduction = 1 - (1 - r1)*(1 - r2)*(1 - r3)...
        """
        selected_interventions = [
            item for item in self.interventions if item["id"] in selected_ids
        ]
        
        if not selected_interventions:
            return {
                "aqi_reduction_pct": 0.0,
                "cost_inr_cr": 0.0,
                "co2_reduction_tonnes": 0.0,
                "days_max": 0
            }
            
        # 1. Diminishing returns calculation
        reduction_fractions = [item["aqi_reduction_pct"] / 100.0 for item in selected_interventions]
        product = 1.0
        for r in reduction_fractions:
            product *= (1.0 - r)
            
        combined_reduction_pct = round((1.0 - product) * 100, 1)
        
        # 2. Sum of costs and CO2 reductions
        total_cost = round(sum(item["cost_inr_cr"] for item in selected_interventions), 2)
        total_co2 = round(sum(item["co2_reduction_tonnes"] for item in selected_interventions), 1)
        
        # 3. Time is determined by the longest implementation timeline
        max_days = max(item["implementation_days"] for item in selected_interventions)
        
        return {
            "aqi_reduction_pct": combined_reduction_pct,
            "cost_inr_cr": total_cost,
            "co2_reduction_tonnes": total_co2,
            "days_max": max_days
        }
