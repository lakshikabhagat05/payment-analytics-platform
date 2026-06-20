from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def run_etl():
    print("ETL job running...")

def run_quality_checks():
    print("Running QA checks...")

with DAG(
    dag_id="payment_pipeline",
    start_date=datetime(2025, 1, 1),
    schedule_interval="@daily",
    catchup=False
) as dag:

    etl = PythonOperator(
        task_id="etl_job",
        python_callable=run_etl
    )

    qa = PythonOperator(
        task_id="qa_checks",
        python_callable=run_quality_checks
    )

    etl >> qa