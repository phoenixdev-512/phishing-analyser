from pydantic import BaseModel, HttpUrl, Field
from typing import List, Optional, Dict, Any

class AnalyzeURLRequest(BaseModel):
    url: str

class AIExplanation(BaseModel):
    score: int = Field(..., description="Safety score determined by AI (0-100)")
    explanation: str = Field(..., description="Concise explanation of the verdict")
    decision: Optional[str] = Field(None, description="AI decision: SAFE_TO_CLICK, CAUTION, or DO_NOT_CLICK")
    alternatives: Optional[List[str]] = Field(default=[], description="Safe alternative URLs if applicable")

class AnalysisResult(BaseModel):
    url: str
    verdict: str = Field(..., description="SAFE, SUSPICIOUS, or MALICIOUS")
    safety_score: int = Field(..., description="0-100 Safety Score")
    risk_breakdown: List[str] = Field(default=[], description="List of risk factors found")
    ai_analysis: Optional[AIExplanation] = None
    signals: dict = Field(default={}, description="Extracted technical signals")
    layers: Dict[str, Any] = Field(default={}, description="Breakdown of scores by layer")
