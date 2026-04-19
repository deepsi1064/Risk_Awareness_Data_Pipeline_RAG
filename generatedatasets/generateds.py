import pandas as pd
import random
from datetime import datetime, timedelta

# -----------------------------
# MASTER DATA
# -----------------------------
cards = ["C101","C102","C103","C104","C105"]
vehicles = ["V201","V202","V203","V204","V205"]
drivers = ["D001","D002","D003","D004","D005"]
locations = ["Chennai","Bangalore","Mumbai"]
merchant_types = ["fuel","toll"]

# -----------------------------
# 1. CARD MASTER
# -----------------------------
card_master_data = []
for i in range(len(cards)):
    card_master_data.append([
        cards[i],
        drivers[i],
        vehicles[i],
        random.choice([4000,5000,6000,7000]),
        random.choice(["active","blocked"]),
        random.choice(locations)
    ])

card_master_df = pd.DataFrame(card_master_data, columns=[
    "card_id","driver_id","vehicle_id","daily_limit","card_status","home_location"
])

card_master_df.to_csv("./data/card_master.csv", index=False)

# -----------------------------
# 2. TRANSACTIONS
# -----------------------------
transactions = []
errors = []

for i in range(1000):
    transaction_id = f"T{i}"
    card_id = random.choice(cards)
    vehicle_id = random.choice(vehicles)
    timestamp = datetime.now() - timedelta(minutes=random.randint(0, 10000))
    location = random.choice(locations)
    merchant = random.choice(merchant_types)
    amount = random.choice([100,200,500,2500,5000,15000])
    status = random.choice(["success","failed"])

    # ---- Inject Errors ----
    # NULL amount
    if random.random() < 0.05:
        amount = None
        errors.append(["transactions.csv", transaction_id, "NULL_VALUE", "amount", "Amount missing"])

    # Negative amount
    if random.random() < 0.05:
        amount = -500
        errors.append(["transactions.csv", transaction_id, "NEGATIVE_VALUE", "amount", "Amount negative"])

    # Invalid timestamp
    if random.random() < 0.03:
        timestamp = "INVALID_DATE"
        errors.append(["transactions.csv", transaction_id, "INVALID_FORMAT", "timestamp", "Wrong date format"])

    transactions.append([
        transaction_id, card_id, vehicle_id, timestamp,
        location, merchant, amount, status
    ])

# Add duplicate rows intentionally
for _ in range(20):
    dup = random.choice(transactions)
    transactions.append(dup)
    errors.append(["transactions.csv", dup[0], "DUPLICATE", "transaction_id", "Duplicate record"])

transactions_df = pd.DataFrame(transactions, columns=[
    "transaction_id","card_id","vehicle_id","timestamp",
    "location","merchant_type","amount","status"
])

transactions_df.to_csv("./data/transactions.csv", index=False)

# -----------------------------
# 3. PIN LOGS
# -----------------------------
pin_logs = []

for i in range(300):
    log_id = f"L{i}"
    card_id = random.choice(cards)
    timestamp = datetime.now() - timedelta(minutes=random.randint(0, 10000))
    attempts = random.choice([1,2,3,4])
    status = "failed" if attempts >= 3 else "success"

    pin_logs.append([log_id, card_id, timestamp, attempts, status])

pin_df = pd.DataFrame(pin_logs, columns=[
    "log_id","card_id","timestamp","attempt_count","status"
])

pin_df.to_csv("./data/pin_logs.csv", index=False)

# -----------------------------
# 4. SOURCE ERRORS
# -----------------------------
errors_df = pd.DataFrame(errors, columns=[
    "file_name","record_id","error_type","column_name","description"
])

errors_df.to_csv("./data/source_errors.csv", index=False)

print("✅ All datasets generated successfully!")