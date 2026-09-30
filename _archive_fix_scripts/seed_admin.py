import requests

# 1. Pirojektii fi Web API Key
PROJECT_ID = "datapulseapp-20237"
API_KEY = "AIzaSyAb1Fbs8Y36BZ8rnIUZBjocc-m0Em_PgcQ"

# 2. Daataa admins fi users haaraa
datapulse_data = {
    "admins": [
        {"id": "admin_uid_01", "email": "admin@datapulse.com", "name": "Super Admin", "role": "super_admin", "status": "active"},
        {"id": "admin_uid_02", "email": "manager@datapulse.com", "name": "Manager", "role": "admin", "status": "active"}
    ],
    "users": [
        {"id": "user_01", "name": "Admin User", "email": "admin@datapulse.com", "role": "admin", "status": "active"},
        {"id": "user_02", "name": "John Doe", "email": "john@example.com", "role": "user", "status": "active"}
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
print("⏳ Daataa admin fi users galchuu jalqabame...")
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

print("🎉 Daataa admin fi users milkaa'inaan galameera!")
