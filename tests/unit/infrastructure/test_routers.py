import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest.mock import Mock

from src.infrastructure.adapters.ingoing.routers import router, get_predict_use_case
# 1. Importamos também o HistoricalDataDTO
from src.application.dtos.dtos import ForecastResponseDTO, HistoricalDataDTO 

app = FastAPI()
app.include_router(router)

client = TestClient(app)

def test_predict_endpoint_success():
    mock_use_case = Mock()
    
    mock_history = [HistoricalDataDTO(date="2024-12-24", quantity=140.0)]
    
    mock_use_case.execute.return_value = ForecastResponseDTO(
        predicted_quantity=145.5,
        history=mock_history
    )

    app.dependency_overrides[get_predict_use_case] = lambda: mock_use_case

    payload = {
        "brand": "Brand_A",
        "hierarchy": "Category_1",
        "date": "2024-12-25"
    }

    response = client.post("/predict", json=payload)

    assert response.status_code == 200
    
    assert response.json() == {
        "predicted_quantity": 145.5,
        "history": [
            {"date": "2024-12-24", "quantity": 140.0}
        ]
    }
    
    mock_use_case.execute.assert_called_once()

    app.dependency_overrides.clear()

def test_predict_endpoint_validation_error():
    app.dependency_overrides[get_predict_use_case] = lambda: Mock()

    payload = {
        "brand": "Brand_A",
        "hierarchy": "Category_1"
    }

    response = client.post("/predict", json=payload)

    assert response.status_code == 422
    assert "date" in response.text

    app.dependency_overrides.clear()

def test_predict_endpoint_domain_error():
    mock_use_case = Mock()
    mock_use_case.execute.side_effect = ValueError("No history found for this product")

    app.dependency_overrides[get_predict_use_case] = lambda: mock_use_case

    payload = {
        "brand": "Brand_Error",
        "hierarchy": "Cat_Error",
        "date": "2024-12-25"
    }

    response = client.post("/predict", json=payload)

    assert response.status_code == 400
    assert response.json() == {"detail": "No history found for this product"}

    app.dependency_overrides.clear()

def test_predict_endpoint_internal_server_error():
    mock_use_case = Mock()
    mock_use_case.execute.side_effect = Exception("Disk failure reading joblib")

    app.dependency_overrides[get_predict_use_case] = lambda: mock_use_case

    payload = {
        "brand": "Brand_A",
        "hierarchy": "Cat_1",
        "date": "2024-12-25"
    }

    response = client.post("/predict", json=payload)

    assert response.status_code == 500
    assert "Internal Server Error: Disk failure" in response.json()["detail"]

    app.dependency_overrides.clear()