from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timedelta
import os
import uuid
import uvicorn
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

import models
import schemas
from database import engine, get_db

# 1. Database uumuu
models.Base.metadata.create_all(bind=engine)

# 2. App fi CORS qindaa'ina
app = FastAPI(title="DataPulse Backend", version="1.0.0")

origins = [
    "https://datapulseapp-20237.web.app",
    "https://datapulseapp-20237-21731.web.app",
    "http://localhost:3000",
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Global Error Handlers
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

# 4. Security & Auth Setup
SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret-key-change-in-render")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(models.User).filter(models.User.email == email).first()
    if user is None:
        raise credentials_exception
    return user

def get_current_admin(current_user: models.User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    return current_user

# 5. DataPulse In-Memory Models & Stores
class RecordModel(BaseModel):
    id: Optional[str] = None
    name: str
    category: Optional[str] = "General"
    price: Optional[float] = 0
    cost: Optional[float] = 0
    stock: Optional[int] = 0
    unit: Optional[str] = "Units"

DP_RECORDS = []
DP_USAGE = {"used": 0, "runs": 0}
DP_AUDIT = []

# 6. Public & DataPulse Routes
@app.get("/")
def root():
    return {"message": "DataPulse Backend is running!", "status": "online", "timestamp": datetime.now().isoformat()}

@app.get("/health")
def health():
    return {"status": "ok", "timestamp": datetime.now().isoformat()}

@app.post("/api/ping")
def ping(data: dict):
    return {"received": data, "reply": "pong from DataPulse"}

@app.post("/api/payment/create")
def create_payment(data: dict):
    return {
        "success": True,
        "message": "Payment request received",
        "amount": data.get("amount", 0),
        "currency": data.get("currency", "ETB")
    }

@app.get("/api/capabilities")
def get_capabilities():
    return [
        {"id": 1, "name": "CSV / Excel Ingest", "category": "INGESTION", "desc": "Ingest data from CSV/Excel"},
        {"id": 2, "name": "REST API Sync", "category": "INGESTION", "desc": "Sync via REST API"},
        {"id": 3, "name": "Join Link Auto", "category": "INGESTION", "desc": "Auto join links"},
        {"id": 4, "name": "IoT Sensor Stream", "category": "INGESTION", "desc": "IoT sensor streams"},
        {"id": 5, "name": "Manual Entry", "category": "INGESTION", "desc": "Manual data entry"},
        {"id": 6, "name": "Auto-Clean", "category": "CLEANING", "desc": "Auto clean data"},
        {"id": 7, "name": "Deduplicate", "category": "CLEANING", "desc": "Remove duplicates"},
        {"id": 8, "name": "Null Imputation", "category": "CLEANING", "desc": "Fill missing values"},
        {"id": 9, "name": "Outlier Removal", "category": "CLEANING", "desc": "Remove outliers"},
        {"id": 10, "name": "Trim & Normalize", "category": "CLEANING", "desc": "Trim and normalize"},
        {"id": 11, "name": "Schema Validation", "category": "CLEANING", "desc": "Validate schema"},
        {"id": 12, "name": "Type Coercion", "category": "CLEANING", "desc": "Coerce data types"},
        {"id": 13, "name": "Descriptive Stats", "category": "ANALYSIS", "desc": "Descriptive statistics"},
        {"id": 14, "name": "Correlation", "category": "ANALYSIS", "desc": "Correlation analysis"},
        {"id": 15, "name": "Linear Regression", "category": "ANALYSIS", "desc": "Linear regression"},
        {"id": 16, "name": "Clustering", "category": "ANALYSIS", "desc": "Clustering algorithms"},
        {"id": 17, "name": "Time Series", "category": "ANALYSIS", "desc": "Time series analysis"},
        {"id": 18, "name": "Cohort Analysis", "category": "ANALYSIS", "desc": "Cohort analysis"},
        {"id": 19, "name": "Distribution", "category": "ANALYSIS", "desc": "Distribution analysis"},
        {"id": 20, "name": "Anomaly Detection", "category": "ANALYSIS", "desc": "Detect anomalies"},
        {"id": 21, "name": "Prediction", "category": "AI/ML", "desc": "Predictive modeling"},
        {"id": 22, "name": "Forecasting", "category": "AI/ML", "desc": "Forecasting models"},
        {"id": 23, "name": "Classification", "category": "AI/ML", "desc": "Classification models"},
        {"id": 24, "name": "NLP Sentiment", "category": "AI/ML", "desc": "NLP sentiment analysis"},
        {"id": 25, "name": "Recommendation", "category": "AI/ML", "desc": "Recommendation systems"},
        {"id": 26, "name": "Decision Tree", "category": "AI/ML", "desc": "Decision tree models"},
        {"id": 27, "name": "KPI Engine", "category": "BUSINESS", "desc": "KPI engine"},
        {"id": 28, "name": "Executive Report", "category": "BUSINESS", "desc": "Executive reporting"},
        {"id": 29, "name": "Smart Alerts", "category": "BUSINESS", "desc": "Smart alerts"},
        {"id": 30, "name": "Dashboard Sync", "category": "BUSINESS", "desc": "Dashboard sync"},
        {"id": 31, "name": "Benchmark", "category": "BUSINESS", "desc": "Benchmarking"},
        {"id": 32, "name": "PII Masking", "category": "SECURITY", "desc": "PII masking"},
        {"id": 33, "name": "Encryption", "category": "SECURITY", "desc": "Data encryption"},
        {"id": 36, "name": "Scheduled Sync", "category": "AUTOMATION", "desc": "Scheduled sync"},
        {"id": 37, "name": "Webhook Trigger", "category": "AUTOMATION", "desc": "Webhook triggers"},
        {"id": 38, "name": "Full Pipeline", "category": "AUTOMATION", "desc": "Full pipeline automation"},
        {"id": 39, "name": "Auto-Report Email", "category": "AUTOMATION", "desc": "Auto report emails"},
        {"id": 40, "name": "Continuous Loop", "category": "AUTOMATION", "desc": "Continuous loop automation"},
    ]

@app.get("/api/records")
def get_records():
    try:
        return {"success": True, "records": DP_RECORDS, "count": len(DP_RECORDS)}
    except Exception as e:
        return {"success": False, "error": str(e), "records": []}

@app.post("/api/records")
def add_record(record: RecordModel):
    try:
        rec = record.dict()
        if not rec.get("id"):
            rec["id"] = "SKU-" + str(uuid.uuid4())[:8].upper()
        DP_RECORDS.append(rec)
        DP_AUDIT.append({"action": "RECORD_ADDED", "target": rec["id"]})
        return {"success": True, "record": rec, "total": len(DP_RECORDS)}
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.delete("/api/records/{record_id}")
def delete_record(record_id: str):
    try:
        global DP_RECORDS
        before = len(DP_RECORDS)
        DP_RECORDS = [r for r in DP_RECORDS if r.get("id") != record_id]
        DP_AUDIT.append({"action": "RECORD_DELETED", "target": record_id})
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
        insights.append({"icon": "fa-chart-line", "color": "sky", "title": "Data Overview", "desc": f"Total records: {stats.get('total_records', 0)}"})
        if stats.get("low_stock_count", 0) > 0:
            insights.append({"icon": "fa-boxes-stacked", "color": "amber", "title": "Low Stock Alert", "desc": f"{stats['low_stock_count']} items are low in stock"})
        top = max(DP_RECORDS, key=lambda r: r.get("price", 0) * r.get("stock", 0)) if DP_RECORDS else None
        if top:
            insights.append({"icon": "fa-star", "color": "purple", "title": "Top Value Item", "desc": f"{top['name']} is the highest value item"})
        return {"success": True, "insights": insights}
    except Exception as e:
        return {"success": False, "error": str(e), "insights": []}

# 7. Database Auth & Admin Routes
@app.post("/register", response_model=schemas.UserResponse)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = get_password_hash(user.password)
    new_user = models.User(email=user.email, hashed_password=hashed_password, role=user.role)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/token", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/api/admin/reports")
def get_admin_reports(
    current_admin: models.User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    users_count = db.query(models.User).count()
    records_count = db.query(models.Record).count()
    return {
        "status": "success",
        "admin_email": current_admin.email,
        "total_users": users_count,
        "total_records": records_count,
        "generated_at": datetime.utcnow()
    }

@app.get("/api/db-records")
def get_db_records(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    records = db.query(models.Record).all()
    return {"success": True, "records": records, "count": len(records)}

# 8. Main block (Render irratti hojjechuuf)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
