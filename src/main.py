import os
from fastapi import FastAPI
from src.infrastructure.adapters.ingoing.routers import router, get_predict_use_case
from src.infrastructure.adapters.outgoing.xgboost_predictor import XGBoostPredictorAdapter
from src.infrastructure.adapters.outgoing.sqlite_repository import SQLiteHistoryRepository
from src.application.use_cases.predict_quantity_use_case import PredictQuantityUseCase

# 1. Define paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "models", "xgboost_final.joblib")
PREPROCESSOR_PATH = os.path.join(BASE_DIR, "models", "preprocessor.joblib")
DB_PATH = os.path.join(BASE_DIR, "data", "api_forecast.db") 

# 2. Instantiate the Infrastructure Adapters (Port implementations)
predictor_adapter = XGBoostPredictorAdapter(
    model_path=MODEL_PATH, 
    preprocessor_path=PREPROCESSOR_PATH
)

history_repo = SQLiteHistoryRepository(
    db_path=DB_PATH
)

# 3. Instantiate the Use Case with ALL injected dependencies
predict_use_case = PredictQuantityUseCase(
    predictor=predictor_adapter,
    history_repo=history_repo
)

# 4. Initialize FastAPI Application
app = FastAPI(
    title="WMS Forecast API",
    description="Clean Architecture XGBoost Inference API for Warehouse Demand",
    version="1.0.0"
)

# 5. Setup Dependency Injection for the Router
app.dependency_overrides[get_predict_use_case] = lambda: predict_use_case

# 6. Include Routers
app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)