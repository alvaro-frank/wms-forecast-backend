from dataclasses import dataclass

@dataclass(frozen=True)
class ProductIdentity:
    """
    Represents the identity and hierarchical categorization of a product.
    """
    brand: str
    hierarchy1: str
    hierarchy2: str
    hierarchy3: str

    def __post_init__(self):
        if not self.brand or not self.hierarchy1:
            raise ValueError("Domain Error: Brand and primary hierarchy (hierarchy1) cannot be empty.")


@dataclass(frozen=True)
class TemporalContext:
    """
    Represents the cyclical and categorical time-based features for a specific prediction moment.
    """
    week_sin: float
    week_cos: float
    month_sin: float
    month_cos: float
    year_sin: float
    year_cos: float
    is_weekend: bool
    is_portuguese_holiday: bool

    def __post_init__(self):
        # Business rule: cyclical time encoded values must strictly fall between -1.0 and 1.0
        cyclical_attributes = [
            self.week_sin, self.week_cos, 
            self.month_sin, self.month_cos, 
            self.year_sin, self.year_cos
        ]
        
        for val in cyclical_attributes:
            if not -1.0 <= val <= 1.0:
                raise ValueError(f"Domain Error: Cyclical time values must be between -1 and 1. Got {val}")


@dataclass(frozen=True)
class HistoricalMovement:
    """
    Represents the historical data, lags, moving averages (EWMA), and differences 
    leading up to the forecast point.
    """
    quantity: float
    lag1: float
    lag2: float
    lag7: float
    lag15: float
    lag30: float
    diff1: float
    diff2: float
    diff7: float
    diff15: float
    diff30: float
    ewma_05: float
    ewma_20: float
    ewma_50: float
    
    def __post_init__(self):
        if self.quantity < 0:
            raise ValueError("Domain Error: Baseline quantity cannot be negative.")


@dataclass(frozen=True)
class ForecastContext:
    """
    The main aggregate root entity containing all necessary information 
    to request a demand forecast for a product.
    """
    product: ProductIdentity
    temporal: TemporalContext
    history: HistoricalMovement


@dataclass(frozen=True)
class ForecastResult:
    """
    Represents the final predicted value computed by the AI model.
    """
    predicted_quantity: float

    def __post_init__(self):
        # Depending on the business rules, a predicted demand might not make sense if negative.
        # We can enforce domain validation here.
        if self.predicted_quantity < 0:
            raise ValueError(f"Domain Error: Predicted quantity cannot be negative. Got {self.predicted_quantity}")