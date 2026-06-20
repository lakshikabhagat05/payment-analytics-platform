import pandas as pd
from sqlalchemy import create_engine

print("Starting Fraud Detection...")

engine = create_engine(
    "postgresql+psycopg2://payment_user:payment_pass@host.docker.internal:5432/payment_db"
)

df = pd.read_sql(
    "SELECT * FROM transactions",
    engine
)

print(f"Transactions Loaded: {len(df)}")

alerts = []

# Rule 1
high_value = df[df["amount"] > 50000]

for _, row in high_value.iterrows():
    alerts.append({
        "transaction_id": row["transaction_id"],
        "fraud_reason": "HIGH_VALUE_TRANSACTION"
    })

# Rule 2
very_high = df[df["amount"] > 100000]

for _, row in very_high.iterrows():
    alerts.append({
        "transaction_id": row["transaction_id"],
        "fraud_reason": "VERY_HIGH_VALUE_TRANSACTION"
    })

alerts_df = pd.DataFrame(alerts)

print(f"Fraud Alerts Generated: {len(alerts_df)}")

alerts_df.to_sql(
    "fraud_alerts",
    engine,
    if_exists="replace",
    index=False
)

print("Fraud alerts loaded successfully")