import pytest
import sqlite3
from src.infrastructure.adapters.outgoing.sqlite_repository import SQLiteHistoryRepository

@pytest.fixture
def temp_db(tmp_path):
    db_path = tmp_path / "test_forecast.db"
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
            'Brand_A', 'Cat_1', '2024-05-15',
            150.0, 10.0, 20.0, 30.0, 40.0, 50.0,
            1.0, 2.0, 3.0, 4.0, 5.0,
            10.5, 11.0, 12.0
        )
    ''')
    conn.commit()
    conn.close()
    
    return str(db_path)

def test_sqlite_repository_get_history_success(temp_db):
    repo = SQLiteHistoryRepository(db_path=temp_db)
    
    history = repo.get_history(brand="Brand_A", hierarchy="Cat_1", date="2024-05-15")
    
    assert history.quantity == 150.0
    assert history.lag1 == 10.0
    assert history.ewma_50 == 12.0

def test_sqlite_repository_get_history_not_found(temp_db):
    repo = SQLiteHistoryRepository(db_path=temp_db)
    
    with pytest.raises(ValueError) as excinfo:
        repo.get_history(brand="Brand_B", hierarchy="Unknown", date="2099-01-01")
        
    assert "No history found for Brand Brand_B" in str(excinfo.value)