import pandas as pd
import os

from validation import validate_transactions
from risk_detection import detect_risks

# -----------------------------
# SETUP OUTPUT FOLDERS
# -----------------------------
os.makedirs("../data/processed", exist_ok=True)
os.makedirs("../data/errors", exist_ok=True)

# -----------------------------
# LOAD DATA
# -----------------------------
transactions = pd.read_csv("../data/transactions.csv")
pin_logs = pd.read_csv("../data/pin_logs.csv")
card_master = pd.read_csv("../data/card_master.csv")

print("✅ Data Loaded")

# -----------------------------
# VALIDATION
# -----------------------------
validation_errors = validate_transactions(transactions)

error_df = pd.DataFrame(validation_errors, columns=["transaction_id","error_type"])
error_df.to_csv("../data/errors/validation_errors.csv", index=False)

print(f"⚠️ Validation Errors Found: {len(validation_errors)}")

# Remove invalid rows
invalid_ids = [e[0] for e in validation_errors]
clean_data = transactions[~transactions["transaction_id"].isin(invalid_ids)]

# -----------------------------
# RISK DETECTION
# -----------------------------
risks = detect_risks(clean_data, pin_logs, card_master)

risk_df = pd.DataFrame(risks, columns=[
    "transaction_id","risks","score","priority"
])

risk_df.to_csv("../data/processed/risk_output.csv", index=False)

print(f"🚨 Risks Detected: {len(risks)}")

# -----------------------------
# SAVE CLEAN DATA
# -----------------------------
clean_data.to_csv("../data/processed/clean_transactions.csv", index=False)

print("✅ Pipeline Completed Successfully")