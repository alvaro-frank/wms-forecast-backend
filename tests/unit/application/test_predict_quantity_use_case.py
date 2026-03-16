import pytest
from unittest.mock import Mock
from src.application.use_cases.predict_quantity_use_case import PredictQuantityUseCase
from src.application.dtos.dtos import ForecastRequestDTO
from src.domain.entities import HistoricalMovement, ForecastResult, ForecastContext

def test_predict_quantity_use_case_orchestration():
    """
    Test if the Use Case correctly orchestrates the flow:
    fetching history, calculating time, and calling the predictor.
    """
    mock_predictor = Mock()
    mock_history_repo = Mock()
    
    dummy_history = HistoricalMovement(
        quantity=100.0, lag1=10, lag2=20, lag7=30, lag15=40, lag30=50,
        diff1=1, diff2=2, diff7=3, diff15=4, diff30=5,
        ewma_05=10.5, ewma_20=11.0, ewma_50=12.0
    )
    mock_history_repo.get_history.return_value = dummy_history
    
    dummy_result = ForecastResult(predicted_quantity=150.5)
    mock_predictor.predict.return_value = dummy_result
    
    use_case = PredictQuantityUseCase(
        predictor=mock_predictor, 
        history_repo=mock_history_repo
    )
    
    request_dto = ForecastRequestDTO(brand="Brand_A", hierarchy="Cat_1", date="2024-05-15")
    response_dto = use_case.execute(request_dto)
    
    assert response_dto.predicted_quantity == 150.5
    
    mock_history_repo.get_history.assert_called_once_with(
        brand="Brand_A", 
        hierarchy="Cat_1", 
        date="2024-05-15"
    )
    
    mock_predictor.predict.assert_called_once()
    
    context_arg = mock_predictor.predict.call_args[0][0]
    assert isinstance(context_arg, ForecastContext)
    assert context_arg.history == dummy_history
    assert context_arg.product.brand == "Brand_A"


def test_predict_quantity_use_case_missing_history_error():
    """
    Test if the use case correctly propagates an error when history is missing 
    or invalid, and ensures the predictor is never called in this scenario.
    """
    mock_predictor = Mock()
    mock_history_repo = Mock()
    
    mock_history_repo.get_history.side_effect = ValueError("History data not found for this product")
    
    use_case = PredictQuantityUseCase(predictor=mock_predictor, history_repo=mock_history_repo)
    request_dto = ForecastRequestDTO(brand="Brand_B", hierarchy="Cat_2", date="2024-05-15")
    
    with pytest.raises(ValueError) as excinfo:
        use_case.execute(request_dto)
        
    assert "History data not found" in str(excinfo.value)
    
    mock_predictor.predict.assert_not_called()