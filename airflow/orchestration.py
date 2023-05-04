import os
import json
import pandas as pd
from prefect import task, flow


@task(name='config')
def get_config(api_key):
    with open('config/{}'.format(api_key)) as f:
        config_data = json.load(f)
    return config_data


@task(name='checks & balances')
def checks_balances(config):
    try:
        file_path = os.path.join(config['data_path'], config['dataset'])
        file_name = os.listdir(file_path)
        file_name = [x for x in file_name if '.csv' in x][0]
        df = pd.read_csv(os.path.join(file_path, file_name), sep='\t')
        df.columns = ['user_id::token', 'item_id::token', 'timestamp::float']
        df['user_id::token'] = df['user_id::token'].astype(str)
        df['item_id::token'] = df['item_id::token'].astype(str)
        df['timestamp::float'] = df['timestamp::float'].astype(int)
        df.to_csv(os.path.join(file_path, file_name.split('.')[0] + '.inter'), sep='\t', index=False)
        return "Success"
    except:
        return "Fail"

@flow(name ='initial flow')
def initial_flow(api_key):
    config = get_config(api_key)
    statement = checks_balances(config)

    return statement
