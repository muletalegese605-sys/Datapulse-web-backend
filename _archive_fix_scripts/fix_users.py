import requests

PROJECT_ID = "datapulseapp-20237"
API_KEY = "AIzaSyAb1Fbs8Y36BZ8rnIUZBjocc-m0Em_PgcQ"
base_url = f"https://firestore.googleapis.com/v1/projects/{PROJECT_ID}/databases/(default)/documents"

# 1. Namoota 5 duraan jiran (ID isaanii) haquuf
ids_to_delete = [
    "0RYHgZ8tpFG7rLijkrRZ",
    "0hTAJTX5Bqj7dZbvzama",
    "QVE0XpsLuhSbu12bLPDu",
    "WjJE8NaMzG8cNgWTCria",
    "vlZtdVVR4vUog2crj04J"
]

print("⏳ Namoota duraan jiran haquu jalqabame...")
for uid in ids_to_delete:
    url = f"{base_url}/users/{uid}?key={API_KEY}"
    res = requests.delete(url)
    if res.status_code == 200:
        print(f"✅ ID {uid} haqameera.")
    else:
        print(f"❌ ID {uid} hin haqamne. Dogoggora: {res.status_code}")

# 2. Namoota 5 haaraa galchuu
new_users = [
    {"id": "user_04", "name": "Hana Tesfaye", "email": "hana@example.com", "role": "user", "status": "active"},
    {"id": "user_05", "name": "Samuel Bekele", "email": "samuel@example.com", "role": "user", "status": "active"},
    {"id": "user_06", "name": "Liya Alemu", "email": "liya@example.com", "role": "user", "status": "active"},
    {"id": "user_07", "name": "Dawit Mekonnen", "email": "dawit.m@example.com", "role": "user", "status": "active"},
    {"id": "user_08", "name": "Meron Tadesse", "email": "meron@example.com", "role": "user", "status": "active"}
]

def convert_to_firestore_value(value):
    if isinstance(value, str): return {"stringValue": value}
    elif isinstance(value, bool): return {"booleanValue": value}
    elif isinstance(value, int): return {"integerValue": value}
    elif isinstance(value, float): return {"doubleValue": value}
    elif isinstance(value, list): return {"arrayValue": {"values": [convert_to_firestore_value(v) for v in value]}}
    elif isinstance(value, dict): return {"mapValue": {"fields": {k: convert_to_firestore_value(v) for k, v in value.items()}}}
    return {"nullValue": None}

print("\n⏳ Namoota 5 haaraa galchuu jalqabame...")
for user in new_users:
    doc_id = user.pop("id")
    url = f"{base_url}/users/{doc_id}?key={API_KEY}"
    fields = {k: convert_to_firestore_value(v) for k, v in user.items()}
    payload = {"fields": fields}
    
    response = requests.patch(url, json=payload)
    if response.status_code == 200:
        print(f"✅ users keessatti {doc_id} galameera.")
    else:
        print(f"❌ users keessatti {doc_id} hin galamne. Dogoggora: {response.status_code}")

print("🎉 Namoonni 5 haaraan milkaa'inaan galameera!")
