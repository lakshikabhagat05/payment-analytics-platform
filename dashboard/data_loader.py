import pandas as pd

def load_transactions(engine):
    return pd.read_sql("SELECT * FROM transactions", engine)

def load_fraud(engine):
    return pd.read_sql("SELECT * FROM fraud_alerts", engine)

def load_reconciliation(engine):
    return pd.read_sql("SELECT * FROM reconciliation_results", engine)