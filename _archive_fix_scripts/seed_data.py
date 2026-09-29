import firebase_admin
from firebase_admin import credentials, firestore
import datetime

# 1. Firebase Admin initialize gochuuf
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

# 2. Firestore client uumuu
db = firestore.client()

print("⏳ Data galchuu jalqabame...")

# 3. Daataa galchuuf qophaa'e (Gosoota dandeettii hojii, data fi kkf)
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

# 4. Firestore keessatti galchuuf (Collection loop)
# Kun collection "features", "categories", "system_settings" ni uuma.
for collection_name, items in datapulse_data.items():
    for item in items:
        # Document ID fayyadamuun adda baasuuf
        doc_id = item.get("id", db.collection(collection_name).document().id)
        db.collection(collection_name).document(doc_id).set(item)
        print(f"✅ {collection_name} keessatti {doc_id} galameera.")

# 5. Metadata dabalataa (Yoo barbaadde)
db.collection("metadata").document("datapulse_info").set({
    "app_name": "DataPulse Web",
    "status": "active",
    "last_updated": firestore.SERVER_TIMESTAMP,
    "total_features": len(datapulse_data["features"]),
    "description": "Sirna bulchiinsa daataa fi dandeettii hojii DataPulse."
})

print("🎉 Daataa hundi milkaa'inaan galameera!")
