import pandas as pd 
import numpy as np
from faker import Faker
from datetime import datetime,timedelta
import random
import os

fake = Faker()
NUM_RECORDS = 100000
payment_methods = ["UPI" ,"CREDIT_CARD","DEBIT_CARD","WALLET","NET_BANKING"]
statuses = ["SUCCESS","FAILED","PENDING"]
merchants = ["Amazon","Flipkart","Swiggy","Zomato","Myntra","Uber","Ola","Reliance","BigBasket","Paytm"]
records = []
print("Generating transactions..")
for i in range(NUM_RECORDS):

    if i % 10000 == 0:
        print(f"Generated {i} records...")

    transaction_id = f"TXN{i+1:06d}"
    customer_id = f"CUST{random.randint(1000,50000)}"
    merchant_id = f"MER{random.randint(100,999)}"
    merchant_name = random.choice(merchants)

    amount = round(random.uniform(10,100000),2)

    payment_method = random.choice(payment_methods)

    status = random.choice(statuses)

    timestamp = fake.date_time_between(
        start_date="-12M",
        end_date="now"
    )

    records.append([
        transaction_id,
        customer_id,
        merchant_id,
        amount,
        payment_method,
        status,
        timestamp
    ])

df = pd.DataFrame(
    records,
    columns=[
        "transaction_id",
        "customer_id",
        "merchant_id",
        "amount",
        "payment_method",
        "status",
        "transaction_timestamp"
    ]
)
# Inject Duplicate transactions

duplicates = df.sample(frac=0.01 ,random_state=42)
df=pd.concat([df,duplicates],ignore_index=True)

# Inject negative numbers 
negative_rows = df.sample(frac=0.002,random_state=1).index
df.loc[negative_rows,"amount"]*= -1
# Inject Invalid status
invalid_rows = df.sample(frac=0.01, random_state =2).index
df.loc[invalid_rows,"status"] ="UNKNOWN"

# Inject Null Merchant IDs
null_rows = df.sample(frac=0.005,random_state=3).index
df.loc[null_rows,"merchant_id"] =None

# Fraud Scenerio 1
# High value transactions
fraud_rows = df.sample(frac=0.005,random_state=4).index
df.loc[fraud_rows,"amount"] = np.random.uniform(50000,150000,size=len(fraud_rows))

# create Output Directory
output_dir = r"data\raw"
os.makedirs(output_dir,exist_ok=True)
output_file = os.path.join(output_dir,"payment_transactions.csv")
df.to_csv(output_file,index=False)
print(f"Dataset generated successfully")
print(f"Rows: {len(df)}")
print(f"saved to: {output_file}")
