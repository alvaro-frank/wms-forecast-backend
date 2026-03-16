import pytest
from src.domain.entities import (
    ProductIdentity,
    TemporalContext,
    HistoricalMovement,
    ForecastResult
)

def test_product_identity_valid():
    """Test valid product identity creation."""
    product = ProductIdentity(brand="Brand_A", hierarchy1="Cat_1", hierarchy2="Sub_1", hierarchy3="Item_1")
    assert product.brand == "Brand_A"
    assert product.hierarchy1 == "Cat_1"

def test_product_identity_invalid():
    """Test if empty brand or hierarchy raises ValueError."""
    with pytest.raises(ValueError) as excinfo:
        ProductIdentity(brand="", hierarchy1="Cat_1", hierarchy2="", hierarchy3="")
    assert "Domain Error: Brand and primary hierarchy" in str(excinfo.value)

def test_temporal_context_valid():
    """Test valid temporal context boundaries."""
    temporal = TemporalContext(
        week_sin=0.5, week_cos=-0.5,
        month_sin=1.0, month_cos=0.0,
        year_sin=-1.0, year_cos=0.5,
        is_weekend=False, is_portuguese_holiday=True
    )
    assert temporal.is_portuguese_holiday is True

def test_temporal_context_invalid_cyclical():
    """Test if cyclical values outside [-1.0, 1.0] raise ValueError."""
    with pytest.raises(ValueError) as excinfo:
        TemporalContext(
            week_sin=1.5, week_cos=0.0, # 1.5 is invalid
            month_sin=0.0, month_cos=0.0,
            year_sin=0.0, year_cos=0.0,
            is_weekend=False, is_portuguese_holiday=False
        )
    assert "Domain Error: Cyclical time values must be between -1 and 1" in str(excinfo.value)

def test_historical_movement_valid():
    """Test valid historical movement creation."""
    history = HistoricalMovement(
        quantity=150.5, lag1=10, lag2=20, lag7=30, lag15=40, lag30=50,
        diff1=1, diff2=2, diff7=3, diff15=4, diff30=5,
        ewma_05=10.5, ewma_20=11.0, ewma_50=12.0
    )
    assert history.quantity == 150.5

def test_historical_movement_invalid_quantity():
    """Test if negative baseline quantity raises ValueError."""
    with pytest.raises(ValueError) as excinfo:
        HistoricalMovement(
            quantity=-5.0, # Negative is invalid
            lag1=10, lag2=20, lag7=30, lag15=40, lag30=50,
            diff1=1, diff2=2, diff7=3, diff15=4, diff30=5,
            ewma_05=10.5, ewma_20=11.0, ewma_50=12.0
        )
    assert "Domain Error: Baseline quantity cannot be negative" in str(excinfo.value)

def test_forecast_result_invalid():
    """Test if negative predicted quantity raises ValueError."""
    with pytest.raises(ValueError) as excinfo:
        ForecastResult(predicted_quantity=-10.5)
    assert "Domain Error: Predicted quantity cannot be negative" in str(excinfo.value)