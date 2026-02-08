from groq import Groq
import os
import asyncio
from typing import Optional
from app.models.schemas import AIExplanation

class AIEngine:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            print("WARNING: GROQ_API_KEY not found in env.")
            self.client = None
        else:
            print(f"AI Engine Configured (Groq). Key length: {len(api_key)}")
            self.client = Groq(api_key=api_key)
            self.model_name = "llama-3.1-8b-instant"

    async def analyze_url(self, url: str, signals: dict, risk_score: int) -> Optional[AIExplanation]:
        if not self.client:
            return AIExplanation(score=risk_score, explanation="AI Analysis unavailable (Missing API Key).")
            
        print(f"Analyzing URL with AI (Groq): {url}")

        prompt = f"""
        You are a Cybersecurity Expert. Analyze this URL: {url}

        Context:
        Technical Signals: {signals}
        - Automated Risk Score: {risk_score}/100 (where 0 is Malicious, 100 is Safe)

        Task:
        1. VALIDATE: Determine if the URL is Phishing, Suspicious, or Safe.
        2. DECIDE: clear decision from ["SAFE_TO_CLICK", "CAUTION", "DO_NOT_CLICK"]
        3. EXPLAIN: concise, jargon-free 1-2 sentences.
        4. ALTERNATIVES: If the URL is phishing a brand (e.g. gøogle.com), provide the legitimate URL (e.g. google.com). If it's a legitimate site, return empty list.

        IMPORTANT: output valid JSON only.
        Format: {{ "score": <int>, "decision": "<string>", "explanation": "<string>", "alternatives": ["<url>"] }}
        """

        try:
            # Run blocking Groq call in a thread to allow async functionality
            # Groq Python client is synchronous by default unless using AsyncGroq (not standard in every env yet, checking docs implied simple switch)
            # We'll use the sync client wrapped in to_thread for simplicity or AsyncGroq if available.
            # To be safe and fast, we'll wrap the sync call.
            
            def get_groq_response():
                chat_completion = self.client.chat.completions.create(
                    messages=[
                        {
                            "role": "user",
                            "content": prompt,
                        }
                    ],
                    model=self.model_name,
                    response_format={"type": "json_object"},
                    max_tokens=300,
                    temperature=0.3, # Low temp for deterministic outputs
                )
                return chat_completion.choices[0].message.content

            response_content = await asyncio.to_thread(get_groq_response)
            
            import json
            result = json.loads(response_content)
            
            return AIExplanation(
                score=result.get("score", risk_score),
                explanation=result.get("explanation", "Could not generate explanation."),
                decision=result.get("decision", "CAUTION"),
                alternatives=result.get("alternatives", [])
            )
            
        except Exception as e:
            print(f"Groq Engine Error Details: {e}")
            return AIExplanation(score=risk_score, explanation="AI Analysis failed due to an error.")
