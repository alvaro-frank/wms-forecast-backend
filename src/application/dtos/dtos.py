from dataclasses import dataclass

@dataclass(frozen=True)
class ForecastRequestDTO:
    brand: str
    hierarchy: str
    date: str

@dataclass(frozen=True)
class ForecastResponseDTO:
    predicted_quantity: float