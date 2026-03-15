from fastapi import APIRouter, Depends, HTTPException
from src.infrastructure.schemas.schemas import ForecastRequestSchema, ForecastResponseSchema
from src.application.dtos.dtos import ForecastRequestDTO
from src.application.use_cases.predict_quantity_use_case import PredictQuantityUseCase

# Changed prefix to match your curl
router = APIRouter(tags=["Demand Forecasting"])

def get_predict_use_case():
    raise NotImplementedError()

@router.post("/predict", response_model=ForecastResponseSchema)
async def predict_demand(
    payload: ForecastRequestSchema, 
    use_case: PredictQuantityUseCase = Depends(get_predict_use_case)
):
    try:
        request_dto = ForecastRequestDTO(**payload.model_dump())
        response_dto = use_case.execute(request_dto)
        return ForecastResponseSchema(predicted_quantity=response_dto.predicted_quantity)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")