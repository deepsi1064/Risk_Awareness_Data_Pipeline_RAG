import pandas as pd

def validate_transactions(df):
    errors = []

    # NULL amount
    null_rows = df[df["amount"].isnull()]
    for _, row in null_rows.iterrows():
        errors.append((row["transaction_id"], "NULL_AMOUNT"))

    # Negative amount
    neg_rows = df[df["amount"] < 0]
    for _, row in neg_rows.iterrows():
        errors.append((row["transaction_id"], "NEGATIVE_AMOUNT"))

    # Invalid timestamp
    for _, row in df.iterrows():
        try:
            pd.to_datetime(row["timestamp"])
        except:
            errors.append((row["transaction_id"], "INVALID_TIMESTAMP"))

    # Duplicate transaction_id
    duplicates = df[df.duplicated("transaction_id")]
    for _, row in duplicates.iterrows():
        errors.append((row["transaction_id"], "DUPLICATE"))

    return errors