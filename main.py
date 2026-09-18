from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from datetime import datetime

app = FastAPI(title="DataPulse Backend", version="1.0.0")

# CORS: Frontend kee (Firebase) akka walqabatu hayyami
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Yeroo ammaa hundi hayyamame; booda URL kee qofa galchi
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

@app.post("/api/ping")
def ping(data: dict):
    return {"received": data, "reply": "pong from DataPulse"}

# Fakkeenya: API kaffaltii (booda TeleBirr/EBC walqabsiisuuf)
@app.post("/api/payment/create")
def create_payment(data: dict):
    # Asitti kaffaltii dhugaa hojjedhu
    return {
        "success": True,
        "message": "Payment request received",
        "amount": data.get("amount", 0),
        "currency": data.get("currency", "ETB")
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
