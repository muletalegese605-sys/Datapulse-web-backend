import requests

# 1. Pirojektii fi Web API Key
PROJECT_ID = "datapulseapp-20237"
API_KEY = "AIzaSyAb1Fbs8Y36BZ8rnIUZBjocc-m0Em_PgcQ"  # Furtuu kee

# 2. Daataa haaraa galchuuf qophaa'e (Collection-oonni duwwaa)
datapulse_data = {
    "users": [
        {"id": "user_01", "name": "Admin User", "email": "admin@datapulse.com", "role": "admin", "status": "active"},
        {"id": "user_02", "name": "John Doe", "email": "john@example.com", "role": "user", "status": "active"}
    ],
    "records": [
        {"id": "rec_01", "title": "Monthly Report", "amount": 1500, "date": "2026-09-28", "category": "Finance"},
        {"id": "rec_02", "title": "Sales Data Q3", "amount": 4500, "date": "2026-09-27", "category": "Sales"},
        {"id": "rec_03", "title": "User Feedback", "amount": 0, "date": "2026-09-26", "category": "Support"}
    ],
    "sales": [
        {"id": "sale_01", "item": "Premium Plan", "price": 99.99, "buyer": "user_02", "date": "2026-09-28"},
        {"id": "sale_02", "item": "Basic Plan", "price": 29.99, "buyer": "user_01", "date": "2026-09-27"}
    ],
    "plans": [
        {"id": "plan_01", "name": "Free Tier", "price": 0, "features": ["10 records", "Basic support"]},
        {"id": "plan_02", "name": "Pro Plan", "price": 29.99, "features": ["Unlimited records", "Priority support"]},
        {"id": "plan_03", "name": "Enterprise", "price": 99.99, "features": ["Custom features", "24/7 support"]}
    ],
    "subscriptions": [
        {"id": "sub_01", "user_id": "user_01", "plan_id": "plan_02", "status": "active", "renewal_date": "2026-10-28"},
        {"id": "sub_02", "user_id": "user_02", "plan_id": "plan_01", "status": "active", "renewal_date": "2026-10-27"}
    ],
    "datasets": [
        {"id": "ds_01", "name": "Customer Feedback", "size": "2.5MB", "owner": "user_01"},
        {"id": "ds_02", "name": "Sales Records 2026", "size": "15MB", "owner": "user_02"}
    ],
    "capabilities": [
        {"id": "cap_01", "name": "Data Export", "enabled": True, "limit": 1000},
        {"id": "cap_02", "name": "API Access", "enabled": True, "limit": 5000},
        {"id": "cap_03", "name": "Real-time Sync", "enabled": False, "limit": 0}
    ]
}

# 3. Firestore REST API endpoint
base_url = f"https://firestore.googleapis.com/v1/projects/{PROJECT_ID}/databases/(default)/documents"

# 4. Data gara Firestore format jijjiiruuf
def convert_to_firestore_value(value):
    if isinstance(value, str):
        return {"stringValue": value}
    elif isinstance(value, bool):
        return {"booleanValue": value}
    elif isinstance(value, int):
        return {"integerValue": value}
    elif isinstance(value, float):
        return {"doubleValue": value}
    elif isinstance(value, list):
        return {"arrayValue": {"values": [convert_to_firestore_value(v) for v in value]}}
    elif isinstance(value, dict):
        return {"mapValue": {"fields": {k: convert_to_firestore_value(v) for k, v in value.items()}}}
    return {"nullValue": None}

# 5. Galchuu
print("⏳ Daataa haaraa galchuu jalqabame...")
for collection_name, items in datapulse_data.items():
    for item in items:
        doc_id = item.pop("id")  # 'id' adda baasuuf
        url = f"{base_url}/{collection_name}/{doc_id}?key={API_KEY}"
        
        fields = {k: convert_to_firestore_value(v) for k, v in item.items()}
        payload = {"fields": fields}
        
        response = requests.patch(url, json=payload)
        
        if response.status_code == 200:
            print(f"✅ {collection_name} keessatti {doc_id} galameera.")
        else:
            print(f"❌ {collection_name} keessatti {doc_id} hin galamne. Dogoggora: {response.status_code}")
            print(f"   Ibsa: {response.text}")

print("🎉 Daataa haaraan hundi milkaa'inaan galameera!")
