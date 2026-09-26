from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from datetime import datetime
import os  # Kun PORT Render irraa fudhachuuf barbaachisa

app = FastAPI(title="DataPulse Backend", version="1.0.0")

# CORS: URL frontend kee (Firebase) qofa hayyami
origins = [
    "https://datapulseapp-20237.web.app",
    "https://datapulseapp-20237-21731.web.app",
    "http://localhost:3000",
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Conflict sirreeffame: "*" bakka bu'ee origins fayyadameera
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============ GLOBAL ERROR HANDLER ============
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": str(exc),
            "error_type": type(exc).__name__,
            "path": str(request.url.path)
        }
    )

@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=400,
        content={"success": False, "error": str(exc), "error_type": "ValueError"}
    )
# ===============================================



@app.get("/")
def root():
    return {"message": "DataPulse Backend is running!", "status": "online"}

@app.get("/health")
def health():
    return {"status": "ok", "timestamp": datetime.now().isoformat()}

# ENDPOINT HAARAA: Capabilities (Kun kan frontend kee gaafatuuf)
@app.get("/api/capabilities")
def get_capabilities():
    return [
        {"id": 1, "name": "CSV / Excel Ingest", "category": "INGESTION", "description": "Auto-clean · chunked"},
        {"id": 2, "name": "REST API Sync", "category": "INGESTION", "description": "Auto-clean · chunked"},
        {"id": 3, "name": "Join Link Auto", "category": "INGESTION", "description": "Google Sheets · CSV · JSON"},
        {"id": 4, "name": "IoT Sensor Stream", "category": "INGESTION", "description": "MQTT · Sensors"},
        {"id": 5, "name": "Manual Entry", "category": "INGESTION", "description": "Forms · Bulk Upload"},
        {"id": 6, "name": "Auto-Clean", "category": "CLEANING", "description": "Smart auto-cleaning"},
        {"id": 7, "name": "Deduplicate", "category": "CLEANING", "description": "Remove duplicates"},
        {"id": 8, "name": "Null Imputation", "category": "CLEANING", "description": "Fill missing values"},
        {"id": 9, "name": "Outlier Removal", "category": "CLEANING", "description": "Detect and remove outliers"},
        {"id": 10, "name": "Trim & Normalize", "category": "CLEANING", "description": "Standardize data"},
        {"id": 11, "name": "Schema Validation", "category": "CLEANING", "description": "Validate data schema"},
        {"id": 12, "name": "Type Coercion", "category": "CLEANING", "description": "Convert data types"},
        {"id": 13, "name": "Descriptive Stats", "category": "ANALYSIS", "description": "Summary statistics"},
        {"id": 14, "name": "Correlation", "category": "ANALYSIS", "description": "Find relationships"},
        {"id": 15, "name": "Linear Regression", "category": "ANALYSIS", "description": "Predictive modeling"},
        {"id": 16, "name": "Clustering", "category": "ANALYSIS", "description": "Group similar data"},
        {"id": 17, "name": "Time Series", "category": "ANALYSIS", "description": "Trend analysis"},
        {"id": 18, "name": "Cohort Analysis", "category": "ANALYSIS", "description": "User segmentation"},
        {"id": 19, "name": "Distribution", "category": "ANALYSIS", "description": "Data distribution"},
        {"id": 20, "name": "Anomaly Detection", "category": "ANALYSIS", "description": "Find anomalies"},
        {"id": 21, "name": "Prediction", "category": "AI/ML", "description": "Predictive analytics"},
        {"id": 22, "name": "Forecasting", "category": "AI/ML", "description": "Time series forecasting"},
        {"id": 23, "name": "Classification", "category": "AI/ML", "description": "Classify data"},
        {"id": 24, "name": "NLP Sentiment", "category": "AI/ML", "description": "Analyze text sentiment"},
        {"id": 25, "name": "Recommendation", "category": "AI/ML", "description": "Recommend items"},
        {"id": 26, "name": "Decision Tree", "category": "AI/ML", "description": "Decision tree model"},
        {"id": 27, "name": "KPI Engine", "category": "BUSINESS", "description": "Track KPIs"},
        {"id": 28, "name": "Executive Report", "category": "BUSINESS", "description": "Generate reports"},
        {"id": 29, "name": "Smart Alerts", "category": "BUSINESS", "description": "Automated alerts"},
        {"id": 30, "name": "Dashboard Sync", "category": "BUSINESS", "description": "Sync dashboards"},
        {"id": 31, "name": "Benchmark", "category": "BUSINESS", "description": "Benchmark metrics"},
        {"id": 32, "name": "PII Masking", "category": "SECURITY", "description": "Mask sensitive data"},
        {"id": 33, "name": "Encryption", "category": "SECURITY", "description": "Encrypt data"},
        {"id": 34, "name": "Access Control", "category": "SECURITY", "description": "Control access"},
        {"id": 35, "name": "Audit Trail", "category": "SECURITY", "description": "Track changes"},
        {"id": 36, "name": "Scheduled Sync", "category": "AUTOMATION", "description": "Schedule syncs"},
        {"id": 37, "name": "Webhook Trigger", "category": "AUTOMATION", "description": "Trigger via webhook"},
        {"id": 38, "name": "Full Pipeline", "category": "AUTOMATION", "description": "End-to-end pipeline"},
        {"id": 39, "name": "Auto-Report Email", "category": "AUTOMATION", "description": "Email reports"},
        {"id": 40, "name": "Continuous Loop", "category": "AUTOMATION", "description": "Continuous processing"}
    ]


@app.post("/api/ping")
def ping(data: dict):
    return {"received": data, "reply": "pong from DataPulse"}

# Fakkeenya: API kaffaltii (booda TeleBirr/EBC walqabsiisuuf)
@app.post("/api/payment/create")
def create_payment(data: dict):
    return {
        "success": True,
        "message": "Payment request received",
        "amount": data.get("amount", 0),
        "currency": data.get("currency", "ETB")
    }

if __name__ == "__main__":
    # Render irratti PORT env var fayyadamuun barbaachisaa dha
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
