import pytest
import numpy as np
from unittest.mock import Mock, patch
from src.infrastructure.adapters.outgoing.xgboost_predictor import XGBoostPredictorAdapter
from src.domain.entities import ForecastContext, ProductIdentity, TemporalContext, HistoricalMovement

@patch('src.infrastructure.adapters.outgoing.xgboost_predictor.joblib.load')
def test_xgboost_adapter_predict_flow(mock_joblib_load):
    """
    Test if the adapter correctly maps the Domain Entity to a DataFrame, 
    applies the preprocessor, calls the model, and reverts the log scale (expm1).
    """
    mock_model = Mock()
    mock_preprocessor = Mock()
    
    mock_joblib_load.side_effect = [mock_model, mock_preprocessor]
    
    mock_preprocessor.transform.return_value = "dummy_transformed_data"
    
    mock_model.predict.return_value = np.array([5.01728])

    adapter = XGBoostPredictorAdapter(model_path="fake.joblib", preprocessor_path="fake.joblib")
    
    product = ProductIdentity(brand="BrandA", hierarchy1="H1", hierarchy2="H2", hierarchy3="H3")
    temporal = TemporalContext(0.1, 0.2, 0.3, 0.4, 0.5, 0.6, False, False)
    history = HistoricalMovement(
        quantity=10, lag1=1, lag2=2, lag7=3, lag15=4, lag30=5, 
        diff1=0.1, diff2=0.2, diff7=0.3, diff15=0.4, diff30=0.5, 
        ewma_05=1.1, ewma_20=1.2, ewma_50=1.3
    )
    context = ForecastContext(product=product, temporal=temporal, history=history)

    result = adapter.predict(context)

    mock_preprocessor.transform.assert_called_once()
    mock_model.predict.assert_called_once_with("dummy_transformed_data")
    
    assert round(result.predicted_quantity) == 150