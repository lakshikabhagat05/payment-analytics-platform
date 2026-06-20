CREATE TABLE IF NOT EXISTS transactions (
    transaction_id VARCHAR(50) PRIMARY KEY,
    customer_id VARCHAR(50),
    merchant_id VARCHAR(50),
    amount NUMERIC(12,2),
    payment_method VARCHAR(50),
    status VARCHAR(50),
    transaction_timestamp TIMESTAMP,
    transaction_date DATE,
    transaction_year INT,
    transaction_month INT,
    amount_category VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS fraud_alerts (
    alert_id SERIAL PRIMARY KEY,
    transaction_id VARCHAR(50),
    fraud_reason VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS reconciliation_results (
    recon_id SERIAL PRIMARY KEY,
    transaction_id VARCHAR(50),
    reconciliation_status VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);