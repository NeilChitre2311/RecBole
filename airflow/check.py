import pandas as pd
import requests
from recbole.quick_start import run_recbole
from prefect import flow,task
import json

import argparse

# create an ArgumentParser object
parser = argparse.ArgumentParser()

# add an argument to the parser
parser.add_argument("input_arg", help="input argument")

# parse the arguments
args = parser.parse_args()

# access the input argument
api_key = args.input_arg

@task
def get_config(api_key):
    with open('config/{}'.format('DqYJjnldMPwthZ28brgrxLkZ003RtWUw') as f:
              return json.loads(f)
    return json.loads('config/{}'.format(api_key)
# print the input argument
print("The input argument is:", input_arg)



