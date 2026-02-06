import random

class MLEngine:
    def __init__(self):
        # In a real app, load model here
        # self.model = joblib.load("model.pkl")
        pass

    def predict(self, url: str, signals: dict) -> float:
        """
        Returns a probability of phishing (0.0 to 1.0)
        """
        # Mock logic to simulate ML
        # Uses signals to bias the random "prediction"
        
        base_risk = 0.1
        
        if signals.get("has_ip"):
            base_risk += 0.4
        if not signals.get("has_https"):
            base_risk += 0.2
        if signals.get("suspicious_keywords"):
            base_risk += 0.3
        
        # Add some noise
        risk = base_risk + (random.random() * 0.1)
        return min(max(risk, 0.0), 1.0)
