import pandas as pd

def detect_risks(transactions, pin_logs, card_master):

    # -----------------------------
    # PREPROCESS
    # -----------------------------
    transactions["timestamp"] = pd.to_datetime(transactions["timestamp"], errors="coerce")
    pin_logs["timestamp"] = pd.to_datetime(pin_logs["timestamp"], errors="coerce")

    risk_dict = {}

    def add_risk(txn_id, risk_type, score):
        if txn_id not in risk_dict:
            risk_dict[txn_id] = {"score": 0, "risks": []}
        
        risk_dict[txn_id]["score"] += score
        risk_dict[txn_id]["risks"].append(risk_type)

    # -----------------------------
    # 1. HIGH AMOUNT
    # -----------------------------
    for _, row in transactions.iterrows():
        if pd.notnull(row["amount"]) and row["amount"] > 10000:
            add_risk(row["transaction_id"], "HIGH_AMOUNT", 30)

    # -----------------------------
    # 2. NIGHT TRANSACTION
    # -----------------------------
    for _, row in transactions.iterrows():
        if pd.notnull(row["timestamp"]) and row["timestamp"].hour < 5:
            add_risk(row["transaction_id"], "NIGHT_TRANSACTION", 20)

    # -----------------------------
    # 3. PIN FAILURE RISK
    # -----------------------------
    risky_cards = pin_logs[pin_logs["attempt_count"] >= 3]["card_id"].unique()

    for _, row in transactions.iterrows():
        if row["card_id"] in risky_cards:
            add_risk(row["transaction_id"], "PIN_FAILURE", 40)

    # -----------------------------
    # 4. BLOCKED CARD USAGE
    # -----------------------------
    blocked_cards = card_master[card_master["card_status"] == "blocked"]["card_id"].values

    for _, row in transactions.iterrows():
        if row["card_id"] in blocked_cards:
            add_risk(row["transaction_id"], "BLOCKED_CARD", 50)

    # -----------------------------
    # 5. RAPID TOLL
    # -----------------------------
    tolls = transactions[transactions["merchant_type"] == "toll"].sort_values("timestamp")

    for i in range(1, len(tolls)):
        curr = tolls.iloc[i]
        prev = tolls.iloc[i-1]

        if curr["card_id"] == prev["card_id"]:
            if pd.notnull(curr["timestamp"]) and pd.notnull(prev["timestamp"]):
                diff = (curr["timestamp"] - prev["timestamp"]).seconds
                if diff < 60:
                    add_risk(curr["transaction_id"], "RAPID_TOLL", 40)

    # -----------------------------
    # 6. LOCATION ANOMALY
    # -----------------------------
    transactions_sorted = transactions.sort_values("timestamp")

    for i in range(1, len(transactions_sorted)):
        curr = transactions_sorted.iloc[i]
        prev = transactions_sorted.iloc[i-1]

        if curr["card_id"] == prev["card_id"]:
            if curr["location"] != prev["location"]:
                if pd.notnull(curr["timestamp"]) and pd.notnull(prev["timestamp"]):
                    time_diff = (curr["timestamp"] - prev["timestamp"]).seconds / 60
                    if time_diff < 120:
                        add_risk(curr["transaction_id"], "LOCATION_ANOMALY", 50)

    # -----------------------------
    # 7. DAILY LIMIT BREACH
    # -----------------------------
    transactions["date"] = transactions["timestamp"].dt.date

    daily_spend = transactions.groupby(["card_id", "date"])["amount"].sum().reset_index()

    for _, row in daily_spend.iterrows():
        card = row["card_id"]
        total = row["amount"]

        limit_row = card_master[card_master["card_id"] == card]

        if not limit_row.empty:
            limit = limit_row["daily_limit"].values[0]

            if total > limit:
                risky_txns = transactions[
                    (transactions["card_id"] == card) &
                    (transactions["date"] == row["date"])
                ]

                for _, txn in risky_txns.iterrows():
                    add_risk(txn["transaction_id"], "LIMIT_BREACH", 30)

    # -----------------------------
    # FINAL OUTPUT
    # -----------------------------
    def get_priority(score):
        if score >= 70:
            return "HIGH"
        elif score >= 40:
            return "MEDIUM"
        else:
            return "LOW"

    final_risks = []

    for txn_id, data in risk_dict.items():
        final_risks.append([
            txn_id,
            ",".join(data["risks"]),
            data["score"],
            get_priority(data["score"])
        ])

    return final_risks