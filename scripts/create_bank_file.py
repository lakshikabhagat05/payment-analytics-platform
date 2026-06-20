import pandas as pd
import random

print("Creating bank transaction file...")

df = pd.read_csv(
    "data/processed/clean_transactions.csv"
)

# Simulate missing records
df = df.sample(
    frac=0.98,
    random_state=42
)

# Simulate amount mismatches
mismatch_rows = df.sample(
    frac=0.01,
    random_state=1
).index

df.loc[mismatch_rows, "amount"] += 100

# Simulate status mismatches
status_rows = df.sample(
    frac=0.005,
    random_state=2
).index

df.loc[status_rows, "status"] = "FAILED"

df.to_csv(
    "data/processed/bank_transactions.csv",
    index=False
)

print(
    f"Bank file created with {len(df)} records"
)