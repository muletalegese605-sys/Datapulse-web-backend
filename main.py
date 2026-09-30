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

from flask_cors import CORS
CORS(app, origins=["https://datapulseapp-20237.web.app", "https://datapulse-web-backend-2.onrender.com"])
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="DataPulse Backend", version="1.0.0")

origins = ["https://datapulseapp-20237.web.app", "http://localhost:3000"]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

# --- Security Setup ---
SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret-key-change-in-render")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password[:72])

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None: raise credentials_exception
    except JWTError: raise credentials_exception
    user = db.query(models.User).filter(models.User.email == email).first()
    if user is None: raise credentials_exception
    return user

def get_current_admin(current_user: models.User = Depends(get_current_user)):
    if current_user.role != "admin": raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    return current_user

# --- Data Models & In-Memory Store ---
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

# --- Public & DataPulse Routes ---
@app.get("/")
def root(): return {"message": "DataPulse Backend is running!", "status": "online", "timestamp": datetime.now().isoformat()}

@app.get("/health")
def health(): return {"status": "ok", "timestamp": datetime.now().isoformat()}

@app.post("/api/ping")
def ping(data: dict): return {"received": data, "reply": "pong from DataPulse"}

@app.post("/api/payment/create")
def create_payment(data: dict):
    return {"success": True, "message": "Payment request received", "amount": data.get("amount", 0), "currency": data.get("currency", "ETB")}

@app.get("/api/capabilities")
def get_capabilities():
    return [{"id": i, "name": f"Capability {i}", "category": "GENERAL", "desc": "Description"} for i in range(1, 41)]

@app.get("/api/records")
def get_records(): return {"success": True, "records": DP_RECORDS, "count": len(DP_RECORDS)}

@app.post("/api/records")
def add_record(record: RecordModel):
    rec = record.dict()
    if not rec.get("id"): rec["id"] = "SKU-" + str(uuid.uuid4())[:8].upper()
    DP_RECORDS.append(rec)
    DP_AUDIT.append({"action": "RECORD_ADDED", "target": rec["id"]})
    return {"success": True, "record": rec, "total": len(DP_RECORDS)}

@app.get("/api/usage")
def get_usage(): return {"success": True, "used": DP_USAGE["used"], "runs": DP_USAGE["runs"]}

@app.post("/api/usage/increment")
def increment_usage():
    DP_USAGE["used"] += 1
    DP_USAGE["runs"] += 1
    return {"success": True, "used": DP_USAGE["used"], "runs": DP_USAGE["runs"]}

@app.get("/api/stats")
def get_stats():
    total_revenue = sum(r.get("price", 0) * r.get("stock", 0) for r in DP_RECORDS)
    total_cost = sum(r.get("cost", 0) * r.get("stock", 0) for r in DP_RECORDS)
    margin = ((total_revenue - total_cost) / total_revenue * 100) if total_revenue > 0 else 0
    low_stock = [r for r in DP_RECORDS if r.get("stock", 0) <= 10]
    return {"success": True, "total_records": len(DP_RECORDS), "total_revenue": total_revenue, "total_cost": total_cost, "margin_percent": round(margin, 2), "low_stock_count": len(low_stock), "low_stock_items": low_stock[:10]}

@app.get("/api/audit")
def get_audit(limit: int = 50): return {"success": True, "audit": DP_AUDIT[-limit:], "count": len(DP_AUDIT)}

@app.get("/api/ai/insights")
def get_insights():
    if not DP_RECORDS: return {"success": True, "insights": []}
    return {"success": True, "insights": [{"icon": "fa-chart-line", "color": "sky", "title": "Data Overview", "desc": f"Total records: {len(DP_RECORDS)}"}]}

# --- Auth & Admin Routes ---
@app.post("/register", response_model=schemas.UserResponse)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user: raise HTTPException(status_code=400, detail="Email already registered")
    new_user = models.User(email=user.email, hashed_password=get_password_hash(user.password), role=user.role)
    db.add(new_user); db.commit(); db.refresh(new_user)
    return new_user

@app.post("/token", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password", headers={"WWW-Authenticate": "Bearer"})
    access_token = create_access_token(data={"sub": user.email}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/api/admin/reports")
def get_admin_reports(current_admin: models.User = Depends(get_current_admin), db: Session = Depends(get_db)):
    return {"status": "success", "admin_email": current_admin.email, "total_users": db.query(models.User).count(), "total_records": db.query(models.Record).count(), "generated_at": datetime.utcnow()}

@app.get("/api/db-records")
def get_db_records(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    records = db.query(models.Record).all()
    return {"success": True, "records": records, "count": len(records)}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
