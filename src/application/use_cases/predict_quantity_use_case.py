from src.domain.entities import ForecastContext, ProductIdentity
from src.domain.services.time_service import TimeService
from src.application.dtos.dtos import ForecastRequestDTO, ForecastResponseDTO
from src.application.ports.ports import IForecastPredictor, IProductHistoryRepository

class PredictQuantityUseCase:
    """
    Use Case responsible for orchestrating the demand forecasting flow.
    It acts as the strict boundary between the delivery mechanism (API) and the business logic.
    """
    
    def __init__(self, predictor: IForecastPredictor, history_repo: IProductHistoryRepository):
        self.predictor = predictor
        self.history_repo = history_repo

    def execute(self, request_dto: ForecastRequestDTO) -> ForecastResponseDTO:
        history = self.history_repo.get_history(
            brand=request_dto.brand, 
            hierarchy=request_dto.hierarchy, 
            date=request_dto.date
        )
        
        temporal = TimeService.get_temporal_context(request_dto.date)
        
        product = ProductIdentity(
            brand=request_dto.brand,
            hierarchy1="UNKNOWN", 
            hierarchy2="UNKNOWN", 
            hierarchy3=request_dto.hierarchy
        )
        
        context = ForecastContext(product=product, temporal=temporal, history=history)
        result = self.predictor.predict(context)

        history_data = self.history_repo.get_last_30_days(
            request_dto.brand, 
            request_dto.hierarchy, 
            request_dto.date
        )
        
        return ForecastResponseDTO(
            predicted_quantity=result.predicted_quantity,
            history=history_data
        )