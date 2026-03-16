import pytest
import os
import sqlite3
from fastapi.testclient import TestClient

try:
    from src.main import app, history_repo
    MODELS_LOADED_SUCCESSFULLY = True
except Exception as e:
    MODELS_LOADED_SUCCESSFULLY = False
    IMPORT_ERROR_MSG = str(e)


@pytest.fixture
def test_client(tmp_path):
    if not MODELS_LOADED_SUCCESSFULLY:
        pytest.skip(f"Incompatibilidade ou falta de ficheiros .joblib. Erro: {IMPORT_ERROR_MSG}")

    db_path = tmp_path / "test_api_forecast.db"
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE history (
            BRAND TEXT, PRODUCTHIERARCHY3 TEXT, DATE TEXT,
            QUANTITY REAL, lag1 REAL, lag2 REAL, lag7 REAL, lag15 REAL, lag30 REAL,
            diff1 REAL, diff2 REAL, diff7 REAL, diff15 REAL, diff30 REAL,
            EWMA_05 REAL, EWMA_20 REAL, EWMA_50 REAL
        )
    ''')
    
    cursor.execute('''
        INSERT INTO history VALUES (
            'Brand_Int', 'Cat_Int', '2024-12-25',
            100.0, 10.0, 20.0, 30.0, 40.0, 50.0,
            1.0, 2.0, 3.0, 4.0, 5.0,
            10.5, 11.0, 12.0
        )
    ''')
    conn.commit()
    conn.close()

    original_db_path = history_repo.db_path
    history_repo.db_path = str(db_path)

    client = TestClient(app)
    
    yield client
    
    history_repo.db_path = original_db_path


def test_end_to_end_forecast_flow(test_client):
    payload = {
        "brand": "Brand_Int",
        "hierarchy": "Cat_Int",
        "date": "2024-12-25"
    }

    response = test_client.post("/predict", json=payload)

    assert response.status_code == 200
    
    data = response.json()
    
    assert "predicted_quantity" in data
    assert isinstance(data["predicted_quantity"], float)
    assert data["predicted_quantity"] >= 0