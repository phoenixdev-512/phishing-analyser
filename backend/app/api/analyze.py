from fastapi import APIRouter, HTTPException
from app.models.schemas import AnalyzeURLRequest, AnalysisResult, AIExplanation
from app.services.aggregator import RiskAggregator
from app.services.ai_engine import AIEngine

router = APIRouter()
aggregator = RiskAggregator()
ai_engine = AIEngine()

@router.post("/analyze", response_model=AnalysisResult)
async def analyze_url(request: AnalyzeURLRequest):
    try:
        # 1. Aggregated Risk Analysis (Fast)
        initial_result = aggregator.aggregate(request.url)
        
        # 2. AI Analysis (Async)
        ai_result = await ai_engine.analyze_url(
            url=request.url,
            signals=initial_result["signals"],
            risk_score=initial_result["safety_score"]
        )
        
        return AnalysisResult(
            url=request.url,
            verdict=initial_result["verdict"],
            safety_score=initial_result["safety_score"],
            risk_breakdown=initial_result["risk_breakdown"],
            signals=initial_result["signals"],
            layers=initial_result.get("layers", {}),
            ai_analysis=ai_result
        )

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
