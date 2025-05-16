# backend/app/routers/analysis.py
from fastapi import APIRouter, HTTPException, Body
from typing import List
from app.models.pydantic_models import PerformanceAnalysisRequest, PerformanceAnalysisResponse
from app.services import gmgn_service

router = APIRouter(
    prefix="/api/v1/analysis",
    tags=["analysis"],
)

@router.post("/performance", response_model=PerformanceAnalysisResponse)
async def get_performance_analysis(
    request_data: PerformanceAnalysisRequest = Body(...)
):
    """
    Analyzes performance for the main wallet and compares with master wallets.
    """
    if not request_data.main_wallet_address and not request_data.master_wallet_addresses:
        raise HTTPException(status_code=400, detail="Either main_wallet_address or master_wallet_addresses must be provided.")
    try:
        data = await gmgn_service.process_wallet_performance_data(
            main_wallet_address=request_data.main_wallet_address,
            master_wallet_addresses=request_data.master_wallet_addresses
        )
        return PerformanceAnalysisResponse(**data)
    except Exception as e:
        print(f"Error in performance analysis endpoint: {e}") # Log error
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

# You might add endpoints to save/load wallet configurations later
# For now, the frontend will manage the list and send it in each request.