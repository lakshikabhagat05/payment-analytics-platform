import pandas as pd
import os

print("Starting Data Transformation...")

# -------------------------------
# Read Raw Data
# -------------------------------

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

input_file = BASE_DIR / "data" / "raw" / "payment_transactions.csv"

df = pd.read_csv(input_file)

print(f"Raw Records: {len(df)}")

# -------------------------------
# Remove Duplicates
# -------------------------------

df = df.drop_duplicates(
    subset=["transaction_id"]
)

print(f"After Duplicate Removal: {len(df)}")

# -------------------------------
# Remove Null Merchant IDs
# -------------------------------

df = df[
    df["merchant_id"].notnull()
]

print(f"After Null Removal: {len(df)}")

# -------------------------------
# Remove Negative Amounts
# -------------------------------

df = df[
    df["amount"] > 0
]

print(f"After Negative Amount Removal: {len(df)}")

# -------------------------------
# Remove Invalid Statuses
# -------------------------------

valid_statuses = [
    "SUCCESS",
    "FAILED",
    "PENDING"
]

df = df[
    df["status"].isin(valid_statuses)
]

print(f"After Status Validation: {len(df)}")

# -------------------------------
# Standardize Timestamp
# -------------------------------

df["transaction_timestamp"] = pd.to_datetime(
    df["transaction_timestamp"]
)

# -------------------------------
# Create Derived Columns
# -------------------------------

df["transaction_date"] = (
    df["transaction_timestamp"]
    .dt.date
)

df["transaction_year"] = (
    df["transaction_timestamp"]
    .dt.year
)

df["transaction_month"] = (
    df["transaction_timestamp"]
    .dt.month
)

# -------------------------------
# Amount Categories
# -------------------------------

def categorize_amount(amount):

    if amount < 1000:
        return "LOW"

    elif amount < 10000:
        return "MEDIUM"

    else:
        return "HIGH"


df["amount_category"] = (
    df["amount"]
    .apply(categorize_amount)
)

# -------------------------------
# Save Clean Data
# -------------------------------

output_dir = BASE_DIR / "data" / "processed"

os.makedirs(
    output_dir,
    exist_ok=True
)

output_file = output_dir / "clean_transactions.csv"

df.to_csv(
    output_file,
    index=False
)

print("\nTransformation Complete")

print(f"Clean Records: {len(df)}")

print(
    f"Saved to: "
    f"{output_file}"
)