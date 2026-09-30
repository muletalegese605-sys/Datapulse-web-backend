import random
from datetime import datetime

# 1. PLANS: Daangaa fi Gatii
PLANS = {
    "Free": {"records": 100, "price_etb": 0, "price_usd": 0},
    "Starter": {"records": 10000, "price_etb": 500, "price_usd": 10},
    "Pro": {"records": 100000, "price_etb": 2000, "price_usd": 40},
    "Enterprise": {"records": "Unlimited", "price_etb": 5000, "price_usd": 100}
}

# 2. PAYMENT GATEWAYS: Mirkaneessuu fi Simulate gochuu
def process_payment(gateway, amount, currency):
    print(f"\n[Payment] Gateway: {gateway} | Gatii: {amount} {currency}")
    
    # Kun simulation qofa. Real world irratti API call ta'a.
    # fkn: requests.post("https://api.chapa.co/v1/transaction/initialize", ...)
    
    if amount == 0:
        return True, "FREE_PLAN_TXN"
    
    # Simulate transaction ID
    txn_id = f"TXN-{random.randint(100000, 999999)}"
    
    # Gateway hundaaf hojjeta jedhee yaadna (Success rate 90%)
    success = random.random() < 0.9 
    
    if success:
        return True, txn_id
    else:
        return False, None

# 3. INVOICE & RECEIPT: Ofumaan uumuu
def generate_invoice(user_email, plan_name, gateway, txn_id, currency):
    waqtii = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    invoice_num = f"INV-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    # Gatii filachuu
    if currency == "ETB":
        amount = PLANS[plan_name]["price_etb"]
    else:
        amount = PLANS[plan_name]["price_usd"]
        
    print("\n" + "="*50)
    print("             DATAPULSE EXECUTIVE DOSSIER")
    print("                 INVOICE & RECEIPT")
    print("="*50)
    print(f"Invoice No: {invoice_num}")
    print(f"Date: {waqtii}")
    print(f"Customer: {user_email}")
    print("-" * 50)
    print(f"Plan: {plan_name}")
    print(f"Record Limit: {PLANS[plan_name]['records']}")
    print(f"Payment Gateway: {gateway}")
    print(f"Transaction ID: {txn_id if txn_id else 'N/A'}")
    print(f"Amount: {amount} {currency}")
    print("-" * 50)
    print("STATUS: ✅ PAYMENT SUCCESSFUL")
    print("="*50 + "\n")
    
    return invoice_num

# 4. MIRKANEESSA: Qormaata adda addaa
def run_test():
    print("--- MIRKANEESSA PAYMENT & SUBSCRIPTION ---")
    
    # Test Case 1: Free Plan (Telebirr)
    print("\n[TEST 1] Free Plan")
    success, txn_id = process_payment("Telebirr", 0, "ETB")
    if success:
        generate_invoice("user@example.com", "Free", "Telebirr", txn_id, "ETB")
    
    # Test Case 2: Starter Plan (Chapa)
    print("\n[TEST 2] Starter Plan - Chapa")
    success, txn_id = process_payment("Chapa", PLANS["Starter"]["price_etb"], "ETB")
    if success:
        generate_invoice("org_a@example.com", "Starter", "Chapa", txn_id, "ETB")
    
    # Test Case 3: Pro Plan (Stripe)
    print("\n[TEST 3] Pro Plan - Stripe")
    success, txn_id = process_payment("Stripe", PLANS["Pro"]["price_usd"], "USD")
    if success:
        generate_invoice("global_user@example.com", "Pro", "Stripe", txn_id, "USD")
        
    # Test Case 4: Enterprise Plan (M-Pesa)
    print("\n[TEST 4] Enterprise Plan - M-Pesa")
    success, txn_id = process_payment("M-Pesa", PLANS["Enterprise"]["price_etb"], "ETB")
    if success:
        generate_invoice("big_org@example.com", "Enterprise", "M-Pesa", txn_id, "ETB")

run_test()
