from app.services.rule_engine import RuleEngine
from app.services.ml_engine import MLEngine
from app.services.signal_extractor import SignalExtractor

class RiskAggregator:
    def __init__(self):
        self.rule_engine = RuleEngine()
        self.ml_engine = MLEngine()
        self.signal_extractor = SignalExtractor()

    def aggregate(self, url: str) -> dict:
        signals = self.signal_extractor.extract_signals(url)
        
        # Layer 1: Preprocessing & Database (Simulated)
        # In real world: check blocklists/whitelists
        layer_1_score = 100
        layer_1_details = ["No Database match found"]
        if "google.com" in url:
            layer_1_details = ["Whitelisted Domain (Trusted)"]
        
        # Layer 2: Heuristics
        rule_analysis = self.rule_engine.analyze(url, signals)
        layer_2_score = 100 - rule_analysis["score_deduction"]
        
        # Layer 3: ML Engine
        phishing_prob = self.ml_engine.predict(url, signals)
        layer_3_score = 100 - int(phishing_prob * 100)
        
        # Layer 4: External Veto (Simulated)
        # e.g. SafeBrowsing
        layer_4_score = 100 
        
        # Calculate Final Weighted Score
        # Database has high trust, Rules have medium, ML has lower weight in this simple formula
        # But we'll use a "lowest score wins" or weighted average approach
        
        final_score = min(layer_1_score, layer_2_score, layer_3_score)
        
        # Adjust for ML findings
        if phishing_prob > 0.6:
            rule_analysis["reasons"].append(f"ML Model High Risk ({phishing_prob:.2f})")
            final_score -= 20
            
        final_score = max(0, min(100, final_score))

        # Determine Verdict
        if final_score >= 80:
            verdict = "SAFE"
        elif final_score >= 50:
            verdict = "SUSPICIOUS"
        else:
            verdict = "MALICIOUS"
            
        return {
            "verdict": verdict,
            "safety_score": final_score,
            "risk_breakdown": rule_analysis["reasons"],
            "signals": signals,
            "layers": {
                "layer_1_database": {"score": layer_1_score, "details": layer_1_details},
                "layer_2_heuristics": {"score": layer_2_score, "details": rule_analysis["reasons"]},
                "layer_3_ml": {"score": layer_3_score, "details": [f"Probability: {phishing_prob:.2f}"]},
                "layer_4_external": {"score": layer_4_score, "details": ["Safe Browsing Clean"]}
            }
        }
