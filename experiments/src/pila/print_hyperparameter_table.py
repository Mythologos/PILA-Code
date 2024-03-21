import glob
import json
import math
import pathlib

import numpy

from lib.pytorch_tools.saver import read_kwargs
from utils.print_table_util import run_main, Column, format_text, format_int, format_float
from pila.print_table import (
    get_best_trial,
    get_best_index,
    get_kwargs,
    get_params
)

def get_hyperparam(name):
    def result(cache):
        kwargs = cache['kwargs']
        if kwargs is not None:
            return kwargs[name]
        else:
            return None
    return result

def get_start_training(cache):
    best_trial = cache['best_trial']
    if best_trial:
        return best_trial.info['start_training']
    else:
        return None

def get_training_setting(name):
    def result(cache):
        start_training = cache['start_training']
        if start_training is not None:
            return start_training[name]
        else:
            return None
    return result

def get_batch_size(cache):
    start_training = cache['start_training']
    if start_training is not None:
        return start_training['batching']['max_tokens']
    else:
        return None

def main():
    run_main(
        columns=[
            Column('Task', 'l', 'label', format_text()),
            Column('$\dmodel$', 'c', 'd_model', format_int()),
            Column('Dropout Rate', 'c', 'dropout', format_float(places=4)),
            Column('Learning Rate', 'c', 'learning_rate', format_float(places=8)),
            Column('Batch Size $B$', 'c', 'batch_size', format_int())
        ],
        callbacks={
            'best_trial' : get_best_trial,
            'best_index' : get_best_index,
            'kwargs' : get_kwargs,
            'params' : get_params,
            'd_model' : get_hyperparam('d_model'),
            'dropout' : get_hyperparam('dropout'),
            'start_training' : get_start_training,
            'learning_rate' : get_training_setting('learning_rate'),
            'batch_size' : get_batch_size
        }
    )

if __name__ == '__main__':
    main()
