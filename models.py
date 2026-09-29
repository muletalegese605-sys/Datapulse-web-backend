from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from database import Base
import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String, default="user") # "admin" yookaan "user"
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Record(Base):
    __tablename__ = "records"
    id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)
    category = Column(String, default="General")
    price = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(Integer, primary_key=True, index=True)
    action = Column(String)
    user_email = Column(String)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
