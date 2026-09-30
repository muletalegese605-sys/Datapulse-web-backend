import os, re

py_path = os.path.expanduser('~/datapulse-backend/main.py')

with open(py_path, 'r') as f:
    content = f.read()

if '/api/records' in content:
    print("⚠️  Endpoints amma jira.")
else:
    new_endpoints = '''

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
'''
    
    if 'if __name__ == "__main__":' in content:
        content = content.replace('if __name__ == "__main__":', new_endpoints + '\nif __name__ == "__main__":', 1)
    else:
        content += new_endpoints
    
    with open(py_path, 'w') as f:
        f.write(content)
    
    print("✅ Endpoints 6 dabalameera!")
    print("📍 /api/records, /api/usage, /api/stats, /api/audit, /api/ai/insights")

