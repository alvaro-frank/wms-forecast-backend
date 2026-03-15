from src.application.dtos.dtos import ForecastRequestDTO, ForecastResponseDTO
from src.application.ports.ports import IForecastPredictor, IProductHistoryRepository
from src.domain.entities import (
    ProductIdentity, 
    ForecastContext
)
from src.domain.services.time_service import TimeService

class PredictQuantityUseCase:
    """
    Use Case responsible for orchestrating the demand forecasting flow.
    It acts as the strict boundary between the delivery mechanism (API) and the business logic.
    """
    
    def __init__(self, predictor: IForecastPredictor, history_repo: IProductHistoryRepository):
        self.predictor = predictor
        self.history_repo = history_repo

    def execute(self, request_dto: ForecastRequestDTO) -> ForecastResponseDTO:
        # 1. Fetch pre-calculated historical data (lags, ewmas) from SQLite
        history = self.history_repo.get_history(
            brand=request_dto.brand, 
            hierarchy=request_dto.hierarchy, 
            date=request_dto.date
        )
        
        # 2. Calculate time features dynamically
        temporal = TimeService.get_temporal_context(request_dto.date)
        
        # 3. Map Product Identity (Filling missing hierarchies with empty strings or default values if your model allows)
        product = ProductIdentity(
            brand=request_dto.brand,
            hierarchy1="UNKNOWN", # Adjust if your DB has this info
            hierarchy2="UNKNOWN", 
            hierarchy3=request_dto.hierarchy
        )
        
        # 4. Assemble Context and Predict
        context = ForecastContext(product=product, temporal=temporal, history=history)
        result = self.predictor.predict(context)
        
        return ForecastResponseDTO(predicted_quantity=result.predicted_quantity)