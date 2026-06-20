import pandas as pd
from sqlalchemy import create_engine

print("Script started")

try:

    df = pd.read_csv(
        "data/processed/clean_transactions.csv"
    )

    print(f"CSV Records Found: {len(df)}")

    engine = create_engine(
        "postgresql+psycopg2://payment_user:payment_pass@localhost:5432/payment_db"
    )

    print("Database connection created")

    df.to_sql(
        "transactions",
        engine,
        if_exists="append",
        index=False
    )

    print(
        f"Loaded {len(df)} records into PostgreSQL"
    )

except Exception as e:
    print("ERROR:")
    print(e)