from abc import ABC, abstractmethod
from src.application.dtos.dtos import ForecastRequestDTO, HistoricalDataDTO
from src.domain.entities import ForecastContext, ForecastResult, HistoricalMovement

class IForecastPredictor(ABC):
    """
    Outbound Port (Interface) for the Machine Learning inference engine.
    
    Any infrastructure adapter (like an XGBoost wrapper) must implement this interface
    to be pluggable into the application use cases.
    """
    
    @abstractmethod
    def predict(self, context: ForecastContext) -> ForecastResult:
        """
        Predicts the future quantity based on the provided domain context.

        Args:
            context (ForecastContext): The aggregate domain entity containing product, 
                                       temporal, and historical information.

        Returns:
            ForecastResult: The domain entity containing the predicted value.
        """
        pass
    
class IProductHistoryRepository(ABC):
    """
    Port (Interface) to retrieve historical movements for a product.
    This allows the application to calculate lags and features automatically.
    """
    @abstractmethod
    def get_history(self, brand: str, hierarchy: str, date: str) -> HistoricalMovement:
        """
        Retrieves the pre-calculated features (lags, ewmas) for a specific product and date.
        """
        pass
    
    def get_last_30_days(self, brand: str, hierarchy: str, target_date: str) -> list[HistoricalDataDTO]:
        """
        Retrieves the last 30 days of historical data for a specific product and date.
        This is used to provide the historical context in the API response.
        """
        pass