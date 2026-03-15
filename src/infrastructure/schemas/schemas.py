from pydantic import BaseModel, Field

class ForecastRequestSchema(BaseModel):
    brand: str = Field(..., description="Brand ID of the product")
    hierarchy: str = Field(..., description="Hierarchy ID of the product")
    date: str = Field(..., description="Target date for forecast (YYYY-MM-DD)")

class ForecastResponseSchema(BaseModel):
    predicted_quantity: float