from datetime import datetime
from airflow import DAG
from airflow.operators.postgres_operator import PostgresOperator

dag = DAG('create_tables_dag',
          description='Create tables in Redshift',
          start_date=datetime.now(),
          schedule_interval='@once',
          max_active_runs=1
)

sql_statement =  open('/home/workspace/airflow/create_tables.sql', 'r').read()

create_tables = PostgresOperator(
    task_id='create_tables',
    postgres_conn_id='redshift',
    dag=dag,
    sql=sql_statement)
