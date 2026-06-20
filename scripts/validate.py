import pandas as pd
from pathlib import Path
import os

print("Starting Data Validation...")

BASE_DIR = Path(__file__).resolve().parent.parent

input_file = BASE_DIR / "data" / "raw" / "payment_transactions.csv"

df = pd.read_csv(input_file)

# Validation metrics
total_records = len(df)
duplicate_transactions = df["transaction_id"].duplicated().sum()
null_merchant_ids = df["merchant_id"].isnull().sum()
negative_amounts = (df["amount"] < 0).sum()
invalid_statuses = (~df["status"].isin(["SUCCESS", "FAILED", "PENDING"])).sum()

# Create report dataframe
report = pd.DataFrame({
    "check_name": [
        "Total Records",
        "Duplicate Transactions",
        "Null Merchant IDs",
        "Negative Amounts",
        "Invalid Statuses"
    ],
    "count": [
        total_records,
        duplicate_transactions,
        null_merchant_ids,
        negative_amounts,
        invalid_statuses
    ]
})

# Save report
report_dir = BASE_DIR / "data" / "reports"
os.makedirs(report_dir, exist_ok=True)

report_file = report_dir / "data_quality_report.csv"

report.to_csv(report_file, index=False)

# Print summary
print("\nData Quality Summary")
print(f"Total records: {total_records}")
print(f"Duplicate Transactions: {duplicate_transactions}")
print(f"Null Merchant IDs: {null_merchant_ids}")
print(f"Negative Amounts: {negative_amounts}")
print(f"Invalid Statuses: {invalid_statuses}")
print(f"\nReport saved to: {report_file}")