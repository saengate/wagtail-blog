# Filename: hello_world2.py
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2019, 9, 28),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
# 'queue': 'bash_queue',
# 'pool': 'backfill',
# 'priority_weight': 10,
# 'end_date': datetime(2016, 1, 1),
}

dag = DAG('hello_world',
    schedule_interval='0 0 * * *' ,
    catchup=False,
    default_args=default_args
)
create_command = 'echo *************************************$(hostname)*************************************'

t1 = BashOperator(
    task_id='task_for_q1',
    bash_command=create_command,
    queue='queue_q1',
    dag=dag
)

t2 = BashOperator(
    task_id= 'task_for_q2',
    bash_command=create_command,
    queue='queue_q2',
    dag=dag
)

t2.set_upstream(t1)
