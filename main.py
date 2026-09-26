from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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
        {"id": 1, "name": "CSV / Excel", "description": "Auto-clean · chunked"},
        {"id": 2, "name": "Link / URL", "description": "Google Sheets · CSV · JSON"},
        {"id": 3, "name": "API Integration", "description": "REST API · Webhooks"},
        {"id": 4, "name": "Database", "description": "PostgreSQL · MongoDB"},
        {"id": 5, "name": "Cloud Storage", "description": "S3 · Google Drive"},
        {"id": 6, "name": "Real-time Stream", "description": "WebSockets · Kafka"},
        {"id": 7, "name": "IoT Devices", "description": "MQTT · Sensors"},
        {"id": 8, "name": "Manual Entry", "description": "Forms · Bulk Upload"}
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
