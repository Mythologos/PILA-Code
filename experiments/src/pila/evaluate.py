import argparse
import itertools
import json
import pathlib
import sys

import more_itertools

from lib.levenshtein import levenshtein_distance
from lib.util import group_by

def load_sequences(path):
    with path.open() as fin:
        for line in fin:
            yield line.split()

class Metric:

    def update(self, hypothesis, reference):
        raise NotImplementedError

    def get_value(self):
        raise NotImplementedError

class MicroAverageMetric(Metric):

    def __init__(self):
        super().__init__()
        self.numerator = 0
        self.denominator = 0

    def update(self, hypothesis, reference):
        numerator, denominator = self.get_parts(hypothesis, reference)
        self.numerator += numerator
        self.denominator += denominator

    def get_value(self):
        return self.numerator / self.denominator

    def get_parts(self, hypothesis, reference):
        raise NotImplementedError

class MinErrorRateMetric(MicroAverageMetric):

    def get_parts(self, hypothesis, reference):
        _, best_numer, best_denom = min(get_error_rates(hypothesis, reference), key=lambda x: x[0])
        return best_numer, best_denom

def get_error_rates(hypothesis, references):
    for reference in references:
        numer = levenshtein_distance(hypothesis, reference)
        denom = len(reference)
        error_rate = numer / denom
        yield error_rate, numer, denom

class MultiExactMatchMetric(MicroAverageMetric):

    def get_parts(self, hypothesis, reference):
        return int(hypothesis in reference), 1

def compute_metrics(named_metrics, pairs):
    for hypothesis, reference in pairs:
        for name, metric in named_metrics:
            metric.update(hypothesis, reference)
    return {
        name : metric.get_value()
        for name, metric in named_metrics
    }

def collapse_group(pairs):
    hypothesis_index = 1
    reference_index = 2
    value = pairs[0][hypothesis_index]
    if not all(pair[hypothesis_index] == value for pair in itertools.islice(pairs, 1, None)):
        raise ValueError
    return value, [pair[reference_index] for pair in pairs]

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--inputs', type=pathlib.Path, required=True)
    parser.add_argument('--hypotheses', type=pathlib.Path, required=True)
    parser.add_argument('--references', type=pathlib.Path, required=True)
    args = parser.parse_args()

    groups = group_by(
        more_itertools.zip_equal(
            load_sequences(args.inputs),
            load_sequences(args.hypotheses),
            load_sequences(args.references)
        ),
        lambda pair: tuple(pair[0])
    )
    pairs = (
        collapse_group(group)
        for input_seq, group in groups.items()
    )

    scores = compute_metrics(
        [
            ('error_rate', MinErrorRateMetric()),
            ('exact_match', MultiExactMatchMetric())
        ],
        pairs
    )
    json.dump(scores, sys.stdout, indent=4)
    print()

if __name__ == '__main__':
    main()
