from src.domain.services.time_service import TimeService

def test_time_service_portuguese_holiday():
    """
    Test if known Portuguese holidays are correctly flagged.
    """
    temporal_context = TimeService.get_temporal_context("2024-04-25")
    
    assert temporal_context.is_portuguese_holiday is True
    assert temporal_context.is_weekend is False

def test_time_service_weekend():
    """
    Test if weekends are correctly flagged.
    """
    temporal_context = TimeService.get_temporal_context("2024-04-27")
    
    assert temporal_context.is_weekend is True
    assert temporal_context.is_portuguese_holiday is False

def test_time_service_regular_day():
    """
    Test a standard workday.
    """
    temporal_context = TimeService.get_temporal_context("2024-04-24")
    
    assert temporal_context.is_weekend is False
    assert temporal_context.is_portuguese_holiday is False

def test_time_service_cyclical_boundaries():
    """
    Test if the generated sin and cos values fall within the strict [-1.0, 1.0] boundary 
    expected by the Domain Entity.
    """
    temporal_context = TimeService.get_temporal_context("2024-01-01")
    
    assert -1.0 <= temporal_context.week_sin <= 1.0
    assert -1.0 <= temporal_context.month_cos <= 1.0
    assert -1.0 <= temporal_context.year_sin <= 1.0
    
    assert isinstance(temporal_context.week_sin, float)