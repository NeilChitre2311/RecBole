import os

import airflow
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.models import Variable

from datetime import date, datetime, timedelta
import pandas as pd


def file_check(**context):
    # print(context['params'])
    # print(context['params']['file_path'])
    file_path = context['params']['file_path']
    print(file_path)
    print("File path correct")
    df = pd.read_csv(file_path,sep = '\t')
    print(df.head(5))
    context["ti"].xcom_push(key="user_df", value=df)
    print("SUCCESS")

def file_check1(**context):
    df = context["ti"].xcom_pull(key="user_df")
    print(df.head())
    print("SUCCESSAA")


with DAG(dag_id='csv_process',
        start_date = datetime(2023, 4, 25),
        schedule_interval=None,
        ) as dag:

    first_task = PythonOperator(task_id="first_task",
                                python_callable=file_check,
                                provide_context=True)
    
    second_task = PythonOperator(task_id="second_task",
                                    python_callable=file_check1,
                                    provide_context=True)
    
    first_task >> second_task