import requests
import json

# 1. Pirojektii fi Web API Key (Kan ati naaf kennite)
PROJECT_ID = "datapulseapp-20237"
API_KEY = "AIzaSyAb1Fbs8Y36BZ8rnIUZBjocc-m0Em_PgcQ"

# 2. Daataa galchuuf qophaa'e (Gosoota dandeettii hojii, data fi kkf)
datapulse_data = {
    "features": [
        {"id": "feat_01", "name": "Data Analysis", "status": "active", "description": "Data qulqulleessuu fi xiinxaluu"},
        {"id": "feat_02", "name": "User Management", "status": "active", "description": "Bulchiinsa fayyadamtootaa"},
        {"id": "feat_03", "name": "Secure Auth", "status": "active", "description": "Nageenya fi mirkaneessa seensaa"},
        {"id": "feat_04", "name": "Data Privacy", "status": "active", "description": "Eeguu odeeffannoo dhuunfaa"},
        {"id": "feat_05", "name": "Real-time Analytics", "status": "active", "description": "Xiinxala yeroo dhugaa"}
    ],
    "categories": [
        {"id": "cat_01", "name": "Finance", "subcategories": ["Budget", "Expense", "Income"]},
        {"id": "cat_02", "name": "Health", "subcategories": ["Fitness", "Nutrition", "Medical"]},
        {"id": "cat_03", "name": "Education", "subcategories": ["Courses", "Exams", "Library"]}
    ],
    "system_settings": [
        {"id": "set_01", "key": "theme", "value": "dark"},
        {"id": "set_02", "key": "version", "value": "1.0.0"},
        {"id": "set_03", "key": "maintenance", "value": False}
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
    elif isinstance(value, list):
        return {"arrayValue": {"values": [convert_to_firestore_value(v) for v in value]}}
    elif isinstance(value, dict):
        return {"mapValue": {"fields": {k: convert_to_firestore_value(v) for k, v in value.items()}}}
    return {"nullValue": None}

# 5. Data galchuu (Loop)
print("⏳ Data galchuu jalqabame...")
for collection_name, items in datapulse_data.items():
    for item in items:
        doc_id = item.pop("id")  # 'id' adda baasuuf
        url = f"{base_url}/{collection_name}/{doc_id}?key={API_KEY}"
        
        # Fields qopheessuu
        fields = {k: convert_to_firestore_value(v) for k, v in item.items()}
        payload = {"fields": fields}
        
        # PATCH fayyadamuun document uumuu ykn haaromsuu
        response = requests.patch(url, json=payload)
        
        if response.status_code == 200:
            print(f"✅ {collection_name} keessatti {doc_id} galameera.")
        else:
            print(f"❌ {collection_name} keessatti {doc_id} hin galamne.")
            print(f"   Dogoggora: {response.text}")

print("🎉 Daataa hundi milkaa'inaan galameera!")
