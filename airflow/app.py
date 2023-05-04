from flask import Flask, request, render_template
import subprocess
# import airflow
# import airflow
# from airflow import DAG
# from airflow.operators.python import PythonOperator
# from airflow.operators.bash import BashOperator
# from airflow.api.client.local_client import Client
import random
import string
import secrets
import json
from orchestration import initial_flow
from multiprocessing import Process
import asyncio

def api_key_generator():
    alphabet = string.ascii_letters + string.digits
    api_key = ''.join(secrets.choice(alphabet) for i in range(32))
    return api_key

def config_creator(api_key,filename):
    data_path = os.path.join(os.getcwd(),'../','data',api_key)
    checkpoint = '../saved/{}'.format(api_key)
    dataset = filename.split('.')[0]
    params = {'data_path':data_path,'dataset':'movielens','checkpoint_dir' : checkpoint}
    return params
    


import os
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            api_key = api_key_generator()
            data_folder = os.path.join(os.getcwd(), os.pardir,'data',api_key,file.filename.split('.')[0])
            #data_folder = os.path.join(os.getcwd(), 'data')
            if not os.path.exists(data_folder):
                os.makedirs(data_folder)
            file.save(os.path.join(data_folder, file.filename))
            subprocess.run(['python', 'test_py.py'])
            print(os.path.join(data_folder, file.filename))
            config = config_creator(api_key,file.filename)
            with open('config/{}'.format(api_key), "w") as fp:
                json.dump(config,fp)
            flow_check = initial_flow(api_key)
            #print(flow_check.is_successful())
            return render_template('success.html',api_key = api_key)
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
