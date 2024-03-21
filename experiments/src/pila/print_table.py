import glob
import json
import math
import pathlib

import numpy

from lib.pytorch_tools.saver import read_kwargs
from utils.print_table_util import run_main, Column, format_text, format_int, format_float

def get_best_trial(cache):
    trials = cache['trials']
    if trials:
        return trials[cache['best_index']]
    else:
        return None

def get_best_index(cache):
    trials = cache['trials']
    if trials:
        return numpy.argmin([
            trial.info['train']['best_validation_scores']['cross_entropy_per_token']
            for trial in trials
        ])
    else:
        return None

def get_kwargs(cache):
    best_trial = cache['best_trial']
    if best_trial:
        return read_kwargs(best_trial.path)
    else:
        return None

def get_params(cache):
    best_trial = cache['best_trial']
    if best_trial:
        return best_trial.info['model_info']['num_parameters']
    else:
        return None

def get_d_model(cache):
    kwargs = cache['kwargs']
    if kwargs is not None:
        return kwargs['d_model']
    else:
        return None

def get_val_perplexity(cache):
    best_trial = cache['best_trial']
    if best_trial:
        return math.exp(best_trial.info['train']['best_validation_scores']['cross_entropy_per_token'])
    else:
        return None

def read_test_data(path):
    for path in glob.glob(str(path / 'eval' / 'pila-*-test' / 'scores.json')):
        with pathlib.Path(path).open() as fin:
            return json.load(fin)

def get_test_scores(cache):
    best_trial = cache['best_trial']
    if best_trial:
        try:
            return read_test_data(best_trial.path)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            return None
    else:
        return None

def get_test_error_rate(cache):
    scores = cache['test_scores']
    if scores is not None:
        return scores['error_rate']
    else:
        return None

def get_test_wer(cache):
    pass
    scores = cache['test_scores']
    if scores is not None:
        return 1 - scores['exact_match']
    else:
        return None

def main():
    run_main(
        columns=[
            Column('Model', 'l', 'label', format_text()),
            Column('Val. Perp. $\\downarrow$', 'c', 'val_perplexity', format_float(places=2)),
            Column('PER $\\downarrow$', 'c', 'test_error_rate', format_float(places=2)),
            Column('WER $\\downarrow$', 'c', 'test_wer', format_float(places=2)),
            #Column('Path', 'l', 'path', format_text())
        ],
        callbacks={
            'best_trial' : get_best_trial,
            'best_index' : get_best_index,
            'kwargs' : get_kwargs,
            'params' : get_params,
            'd_model' : get_d_model,
            'val_perplexity' : get_val_perplexity,
            'test_scores' : get_test_scores,
            'test_error_rate' : get_test_error_rate,
            'test_wer' : get_test_wer,
            'path' : lambda cache: cache['best_trial'].path
        }
    )

if __name__ == '__main__':
    main()
