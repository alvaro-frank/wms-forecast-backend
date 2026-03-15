import pandas as pd
import joblib
from src.application.ports.ports import IForecastPredictor
from src.domain.entities import ForecastContext, ForecastResult
import numpy as np

class XGBoostPredictorAdapter(IForecastPredictor):
    """
    Concrete implementation of the ML predictor port using XGBoost.
    This adapter encapsulates all pandas and joblib dependencies.
    """
    
    def __init__(self, model_path: str, preprocessor_path: str):
        """
        Loads the pre-trained model and preprocessor artifacts into memory.
        """
        self.model = joblib.load(model_path)
        self.preprocessor = joblib.load(preprocessor_path)

    def predict(self, context: ForecastContext) -> ForecastResult:
        """
        Maps the domain context into the exact feature array expected by the pipeline,
        executes the inference, and returns a domain result.
        """
        # 1. Map Domain Entity back to the exact feature names and order required
        features = {
            'QUANTITY': context.history.quantity,
            'lag1': context.history.lag1,
            'diff1': context.history.diff1,
            'EWMA_05': context.history.ewma_05,
            'EWMA_20': context.history.ewma_20,
            'EWMA_50': context.history.ewma_50,
            'Week sin': context.temporal.week_sin,
            'Week cos': context.temporal.week_cos,
            'Month sin': context.temporal.month_sin,
            'Month cos': context.temporal.month_cos,
            'Year sin': context.temporal.year_sin,
            'Year cos': context.temporal.year_cos,
            'is_weekend': context.temporal.is_weekend,
            'is_portuguese_holiday': context.temporal.is_portuguese_holiday,
            'lag2': context.history.lag2,
            'lag7': context.history.lag7,
            'lag15': context.history.lag15,
            'lag30': context.history.lag30,
            'diff2': context.history.diff2,
            'diff7': context.history.diff7,
            'diff15': context.history.diff15,
            'diff30': context.history.diff30,
            'BRAND': context.product.brand,
            'PRODUCTHIERARCHY3': context.product.hierarchy3,
            'PRODUCTHIERARCHY1': context.product.hierarchy1,
            'PRODUCTHIERARCHY2': context.product.hierarchy2,
            'is_pre_christmas': 0,
            'days_to_christmas': 30,
            'is_post_holiday_slump': 0,
            'is_payday_zone': 0,
            'is_black_friday_week': 0
        }

        # 2. Convert to DataFrame (infrastructure detail)
        df_input = pd.DataFrame([features])
        
        # 3. Apply preprocessing pipeline
        df_transformed = self.preprocessor.transform(df_input)
        
        # 4. Predict using the XGBoost model
        log_prediction = self.model.predict(df_transformed)[0]
        real_prediction = np.expm1(log_prediction)
        
        # 5. Return mapped back to a Domain Entity
        return ForecastResult(predicted_quantity=float(real_prediction))