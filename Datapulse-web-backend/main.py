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



# ============ DATA ENDPOINTS ============
from pydantic import BaseModel
from typing import Optional, List
import json

# In-memory store (booda database waliin walqabsiisuu dandeessa)
DP_RECORDS = []
DP_USAGE = {"used": 0, "runs": 0}
DP_AUDIT = []

class RecordModel(BaseModel):
    id: Optional[str] = None
    name: str
    category: Optional[str] = "General"
    price: Optional[float] = 0
    cost: Optional[float] = 0
    stock: Optional[int] = 0
    unit: Optional[str] = "Units"

@app.get("/api/records")
def get_records():
    try:
        return {"success": True, "records": DP_RECORDS, "count": len(DP_RECORDS)}
    except Exception as e:
        return {"success": False, "error": str(e), "records": []}

@app.post("/api/records")
def add_record(record: RecordModel):
    try:
        import uuid
        rec = record.dict()
        if not rec.get("id"):
            rec["id"] = "SKU-" + str(uuid.uuid4())[:8].upper()
        DP_RECORDS.append(rec)
        DP_AUDIT.append({"action": "RECORD_ADDED", "target": rec["id"], "timestamp": datetime.now().isoformat()})
        return {"success": True, "record": rec, "total": len(DP_RECORDS)}
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.delete("/api/records/{record_id}")
def delete_record(record_id: str):
    try:
        global DP_RECORDS
        before = len(DP_RECORDS)
        DP_RECORDS = [r for r in DP_RECORDS if r.get("id") != record_id]
        DP_AUDIT.append({"action": "RECORD_DELETED", "target": record_id, "timestamp": datetime.now().isoformat()})
        return {"success": True, "deleted": before - len(DP_RECORDS)}
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.get("/api/usage")
def get_usage():
    try:
        return {"success": True, "used": DP_USAGE["used"], "runs": DP_USAGE["runs"]}
    except Exception as e:
        return {"success": False, "error": str(e), "used": 0, "runs": 0}

@app.post("/api/usage/increment")
def increment_usage():
    try:
        DP_USAGE["used"] += 1
        DP_USAGE["runs"] += 1
        return {"success": True, "used": DP_USAGE["used"], "runs": DP_USAGE["runs"]}
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.get("/api/stats")
def get_stats():
    try:
        total_revenue = sum(r.get("price", 0) * r.get("stock", 0) for r in DP_RECORDS)
        total_cost = sum(r.get("cost", 0) * r.get("stock", 0) for r in DP_RECORDS)
        margin = ((total_revenue - total_cost) / total_revenue * 100) if total_revenue > 0 else 0
        low_stock = [r for r in DP_RECORDS if r.get("stock", 0) <= 10]
        return {
            "success": True,
            "total_records": len(DP_RECORDS),
            "total_revenue": total_revenue,
            "total_cost": total_cost,
            "margin_percent": round(margin, 2),
            "low_stock_count": len(low_stock),
            "low_stock_items": low_stock[:10]
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.get("/api/audit")
def get_audit(limit: int = 50):
    try:
        return {"success": True, "audit": DP_AUDIT[-limit:], "count": len(DP_AUDIT)}
    except Exception as e:
        return {"success": False, "error": str(e), "audit": []}

@app.get("/api/ai/insights")
def get_insights():
    try:
        if not DP_RECORDS:
            return {"success": True, "insights": []}
        insights = []
        stats = get_stats()
        insights.append({"icon": "fa-chart-line", "color": "sky", "title": "Balanced margin", "text": "Your " + str(stats.get("margin_percent", 0)) + "% margin is in line with expectations."})
        if stats.get("low_stock_count", 0) > 0:
            insights.append({"icon": "fa-boxes-stacked", "color": "amber", "title": str(stats["low_stock_count"]) + " items low on stock", "text": "Restock soon to avoid stockouts."})
        top = max(DP_RECORDS, key=lambda r: r.get("price", 0) * r.get("stock", 0))
        insights.append({"icon": "fa-star", "color": "purple", "title": "Top item: " + str(top.get("name", "Unknown")), "text": "Contributes ETB " + str(top.get("price", 0) * top.get("stock", 0)) + " of projected revenue."})
        return {"success": True, "insights": insights}
    except Exception as e:
        return {"success": False, "error": str(e), "insights": []}

# ========================================

if __name__ == "__main__":
    # Render irratti PORT env var fayyadamuun barbaachisaa dha
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
