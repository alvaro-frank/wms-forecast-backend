import sqlite3
import pandas as pd
from src.application.dtos.dtos import HistoricalDataDTO
from src.application.ports.ports import IProductHistoryRepository
from src.domain.entities import HistoricalMovement

class SQLiteHistoryRepository(IProductHistoryRepository):
    def __init__(self, db_path: str):
        self.db_path = db_path

    def get_history(self, brand: str, hierarchy: str, date: str) -> HistoricalMovement:
        """
        Queries the SQLite DB and returns the features for the specific record.
        Note: If your DB already has the features calculated, we just fetch them.
        """
        conn = sqlite3.connect(self.db_path)
        
        query = """
            SELECT * FROM history 
            WHERE BRAND = ? AND PRODUCTHIERARCHY3 = ? AND DATE = ?
            LIMIT 1
        """
        df = pd.read_sql_query(query, conn, params=(brand, hierarchy, date))
        conn.close()

        if df.empty:
            raise ValueError(f"No history found for Brand {brand} and Hierarchy {hierarchy} on date {date}")

        row = df.iloc[0]
        
        return HistoricalMovement(
            quantity=float(row.get('QUANTITY', 0)),
            lag1=float(row.get('lag1', 0)),
            lag2=float(row.get('lag2', 0)),
            lag7=float(row.get('lag7', 0)),
            lag15=float(row.get('lag15', 0)),
            lag30=float(row.get('lag30', 0)),
            diff1=float(row.get('diff1', 0)),
            diff2=float(row.get('diff2', 0)),
            diff7=float(row.get('diff7', 0)),
            diff15=float(row.get('diff15', 0)),
            diff30=float(row.get('diff30', 0)),
            ewma_05=float(row.get('EWMA_05', 0)),
            ewma_20=float(row.get('EWMA_20', 0)),
            ewma_50=float(row.get('EWMA_50', 0))
        )
        
    def get_last_30_days(self, brand: str, hierarchy: str, target_date: str) -> list[HistoricalDataDTO]:
        query = """
            SELECT date, quantity 
            FROM history 
            WHERE brand = ? AND PRODUCTHIERARCHY3 = ? AND date < ?
            ORDER BY date DESC
            LIMIT 30
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query, (brand, hierarchy, target_date))
            rows = cursor.fetchall()
            # Revertemos para vir por ordem cronológica (mais antigo -> mais recente)
            return [HistoricalDataDTO(date=row[0], quantity=row[1]) for row in reversed(rows)]