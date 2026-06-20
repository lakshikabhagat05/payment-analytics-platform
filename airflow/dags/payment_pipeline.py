from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG(
    dag_id="payment_pipeline",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    tags=["payments", "etl"]
) as dag:

    validate_task = BashOperator(
        task_id="validate_task",
        bash_command="python /opt/airflow/project/scripts/validate.py"
    )

    transform_task = BashOperator(
        task_id="transform_task",
        bash_command="python /opt/airflow/project/scripts/transform.py"
    )

    load_postgres_task = BashOperator(
        task_id="load_postgres_task",
        bash_command="python /opt/airflow/project/scripts/load_postgres.py"
    )

    fraud_detection_task = BashOperator(
        task_id="fraud_detection_task",
        bash_command="python /opt/airflow/project/scripts/fraud_detection.py"
    )

    reconciliation_task = BashOperator(
        task_id="reconciliation_task",
        bash_command="python /opt/airflow/project/scripts/reconcile.py"
    )

    (
        validate_task
        >> transform_task
        >> load_postgres_task
        >> fraud_detection_task
        >> reconciliation_task
    )