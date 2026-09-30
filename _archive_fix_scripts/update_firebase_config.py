import re

with open('index.html', 'r') as f:
    html = f.read()

# Koodii Firebase Config haaraa
new_config = """const firebaseConfig = {
  apiKey: "AIzaSyAb1Fbs8Y36BZ8rnIUZBjocc-m0Em_PgcQ",
  authDomain: "datapulseapp-20237.firebaseapp.com",
  databaseURL: "https://datapulseapp-20237-default-rtdb.europe-west1.firebasedatabase.app",
  projectId: "datapulseapp-20237",
  storageBucket: "datapulseapp-20237.firebasestorage.app",
  messagingSenderId: "459433026519",
  appId: "1:459433026519:web:102f1f951bcb91d306e192",
  measurementId: "G-RFN5ZZTE6W"
};"""

# Firebase Config duraan ture barbaaduu fi bakka buusuu
pattern = re.compile(r"const firebaseConfig\s*=\s*\{.*?\};", re.DOTALL)

if pattern.search(html):
    html = pattern.sub(new_config, html, count=1)
    with open('index.html', 'w') as f:
        f.write(html)
    print("✅ Firebase Config milkaa'inaan haaromeera!")
else:
    print("❌ Dogoggora: Firebase Config hin argamne. Maaloo harkaan sirreessi.")
