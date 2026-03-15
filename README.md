# 📈 WMS Forecast System - Backend

![CI Status](https://github.com/alvaro-frank/wms-forecast-backend/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-009688?logo=fastapi&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED?logo=docker&logoColor=white)
![XGBoost](https://img.shields.io/badge/Model-XGBoost-blue)
![SQLite](https://img.shields.io/badge/DB-SQLite-003B57?logo=sqlite&logoColor=white)

A production-grade Warehouse Management System (WMS) demand forecasting service. This project implements a Machine Learning engine (XGBoost) to predict future product quantities, served via a high-performance FastAPI backend. It strictly follows **Clean Architecture** principles to ensure the core business logic remains decoupled from the ML inference engine, database operations, and the web framework.

## 📂 Project Structure
```text
├── data/                   # Local database storage
│   └── api_forecast.db     # SQLite database for historical/forecast data
├── models/                 # Pre-trained ML Models and Pipelines
│   ├── preprocessor.joblib # Scikit-learn data preprocessor
│   └── xgboost_final.joblib# Trained XGBoost forecasting model
├── src/
│   ├── application/        # Application Logic (Use Cases & DTOs)
│   │   ├── dtos/           # Data Transfer Objects (ForecastRequestDTO)
│   │   ├── ports/          # Interfaces for Outbound Adapters (Predictor, DB)
│   │   └── use_cases/      # Business logic (PredictQuantityUseCase)
│   ├── domain/             # Business Core (Pure Entities)
│   │   ├── entities.py     # Core domain models
│   │   └── services/       # Domain services (e.g., time_service.py)
│   ├── infrastructure/     # Technical Details & External Integrations
│   │   ├── adapters/       # Implementation of Ports
│   │   │   ├── ingoing/    # FastAPI Routers (routers.py)
│   │   │   └── outgoing/   # XGBoost Engine & SQLite Repository
│   │   └── schemas/        # Pydantic Schemas for API validation
│   └── main.py             # Application entry point & DI Container
├── tests/                  # Automated Test Suite
├── Dockerfile              # Container image definition
├── docker-compose.yml      # Service orchestration
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
```

## 🛠️ Setup & Requirements

- `Python 3.9+`
- `Docker` and `Docker Compose`

1. **Clone the repository**
```bash
git clone [https://github.com/alvaro-frank/wms-forecast-backend.git](https://github.com/alvaro-frank/wms-forecast-backend.git)
cd wms-forecast-backend
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

## ⚡ Quick Start

To run the API using **Docker** (recommended):

```bash
docker-compose up --build
```

The API will be available at `http://localhost:8000`. You can access the interactive documentation at `http://localhost:8000/docs`.

To run **locally**:

```bash
python -m src.main
```

## 🏃 Usage & API Specification

The primary endpoint is `POST /predict`.

To run locally without Docker:
```bash
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

**Request Payload Example**:
```bash
{
  "brand": "1487.0",
  "hierarchy": "1060000100001.0",
  "date": "2024-12-01"
}
```

**Response Payload Example**:
```bash
{
  "predicted_quantity": 35.14
}
```

## 🧠 Methodology

**Machine Learning Engine**

The forecasting logic is driven by a trained machine learning pipeline optimized for time-series and categorical demand data.

1. **Preprocessing**: Incoming requests are transformed using a fitted `preprocessor.joblib` pipeline, handling categorical encoding (Brand, Hierarchy) and temporal feature extraction based on the target date.
2. **Inference**: A highly optimized `xgboost_final.joblib` model executes the prediction. Tree-based models like XGBoost provide robust performance for tabular WMS data without the need for GPU acceleration in production.
3. **Data Persistence**: Historical records or forecast logs are managed via a lightweight `SQLite` database, abstracted behind repository ports to allow seamless future migration to PostgreSQL or MySQL.

## 🧪 Testing

The project maintains high reliability through a tiered testing strategy:

```bash
# Run all tests
pytest

# Run with coverage logs
pytest -s -v
```

- **Domain Tests**: Validate rotation math and volume calculations.
- **Application Tests**: Mock the AI to test the packing orchestration logic.
- **Infrastructure Tests**: Verify the ONNX adapter, action masking, and FastAPI routing.
- **Integration Tests**: Full end-to-end flow using real .onnx model files.

## ⚙️ CI/CD Pipeline

The project includes a GitHub Actions workflow that automates the quality gate:

- **Linting**: Ensures PEP8 compliance.
- **Automated Testing**: Executes the full pytest suite on every push.
- **Build Verification**: Ensures the Docker image builds successfully.

## 🐳 Docker Support

The application is optimized for containerization:

- **Lightweight**: Uses `python:3.9-slim` to minimize image size and reduce the attack surface.
- **Production-Ready**: Uses `uvicorn` as a high-performance ASGI server to handle asynchronous API requests.
- **Isolated Inference**: The **XGBoost** and **Scikit-Learn** machine learning pipelines are CPU-optimized for efficient cloud deployment, requiring no heavy GPU drivers.
- **Data Persistence**: Uses Docker volumes to ensure the local SQLite database (`data/api_forecast.db`) safely persists its history across container restarts.
