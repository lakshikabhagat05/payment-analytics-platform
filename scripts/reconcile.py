import pandas as pd
from pathlib import Path
from sqlalchemy import create_engine

print("Starting Reconciliation...")
BASE_DIR = Path(__file__).resolve().parent.parent

gateway_file = BASE_DIR / "data" / "processed" / "clean_transactions.csv"

bank_file = BASE_DIR / "data" / "processed" / "bank_transactions.csv"

gateway = pd.read_csv(gateway_file)
bank = pd.read_csv(bank_file)

results = []

bank_lookup = bank.set_index(
    "transaction_id"
)

for _, row in gateway.iterrows():

    txn_id = row["transaction_id"]

    if txn_id not in bank_lookup.index:

        results.append({
            "transaction_id": txn_id,
            "reconciliation_status": "MISSING_IN_BANK"
        })

        continue

    bank_row = bank_lookup.loc[txn_id]

    if row["amount"] != bank_row["amount"]:

        results.append({
            "transaction_id": txn_id,
            "reconciliation_status": "AMOUNT_MISMATCH"
        })

    elif row["status"] != bank_row["status"]:

        results.append({
            "transaction_id": txn_id,
            "reconciliation_status": "STATUS_MISMATCH"
        })

engine = create_engine(
    "postgresql+psycopg2://payment_user:payment_pass@host.docker.internal:5432/payment_db"
)


results_df = pd.DataFrame(results)

print(
    f"Issues Found: {len(results_df)}"
)

results_df.to_sql(
    "reconciliation_results",
    engine,
    if_exists="append",
    index=False
)

print(
    "Reconciliation complete"
)