from flask import Flask, request, render_template
import subprocess
import airflow
import airflow
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.api.client.local_client import Client

import random
import string

def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


import os
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            data_folder = os.path.join(os.getcwd(), 'data')
            if not os.path.exists(data_folder):
                os.makedirs(data_folder)
            file.save(os.path.join(data_folder, file.filename))
            subprocess.run(['python', 'test_py.py'])
            print(os.path.join(data_folder, file.filename))
            c = Client(None, None)
            c.trigger_dag(dag_id='csv_process', run_id=randomString(), conf={'file_path': os.path.join(data_folder, file.filename)})
            return 'Script executed successfully!'
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
