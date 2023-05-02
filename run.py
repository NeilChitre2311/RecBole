from recbole.quick_start import run_recbole, run_recboles

from recbole.config import Config
import os
data_path = os.path.join(os.getcwd(),'data')
checkpoint = 'saved/api_key'

params = {'data_path':data_path,'dataset':'movielens','checkpoint_dir' : checkpoint}
config = Config(
        model='BPR',
        config_dict=params,
    )


run_recbole(model = 'BPR',config_dict = params)

