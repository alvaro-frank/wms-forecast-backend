import numpy as np
import pandas as pd
import holidays
from src.domain.entities import TemporalContext

class TimeService:
    """
    Domain Service responsible for translating a simple calendar date 
    into the complex cyclical and categorical temporal features required by the AI.
    """
    
    @staticmethod
    def get_temporal_context(date_str: str) -> TemporalContext:
        """
        Converts a date string (YYYY-MM-DD) into a TemporalContext entity.
        Calculations match exactly the pipeline from the training phase (features.py).
        """
        # Convert string to Pandas Timestamp to guarantee math parity with training
        date = pd.to_datetime(date_str)
        timestamp = date.timestamp()
        
        # 1. Constants matching features.py exactly
        day = 24 * 60 * 60 
        week = 7 * day 
        month = 30.44 * day 
        year = 365.2425 * day 
        
        # 2. Cyclical Encoding (Sin/Cos)
        week_sin = np.sin(timestamp * (2 * np.pi / week))
        week_cos = np.cos(timestamp * (2 * np.pi / week))
        
        month_sin = np.sin(timestamp * (2 * np.pi / month))
        month_cos = np.cos(timestamp * (2 * np.pi / month))
        
        year_sin = np.sin(timestamp * (2 * np.pi / year))
        year_cos = np.cos(timestamp * (2 * np.pi / year))
        
        # 3. Categorical Flags
        # Weekday: 0=Mon, ..., 5=Sat, 6=Sun. Weekend is >= 5.
        is_weekend = date.weekday() >= 5
        
        # Check if it's a Portuguese holiday
        pt_holidays = holidays.Portugal()
        is_portuguese_holiday = date in pt_holidays
        
        # 4. Return the strict Domain Entity
        return TemporalContext(
            week_sin=float(week_sin),
            week_cos=float(week_cos),
            month_sin=float(month_sin),
            month_cos=float(month_cos),
            year_sin=float(year_sin),
            year_cos=float(year_cos),
            is_weekend=bool(is_weekend),
            is_portuguese_holiday=bool(is_portuguese_holiday)
        )