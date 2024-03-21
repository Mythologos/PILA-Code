import dataclasses

from .model_util import SequenceToSequenceModelInterface
from .batching import (
    group_into_batches,
    group_sources_into_batches
)

def add_batching_arguments(group):
    group.add_argument('--batching-max-tokens', type=int, required=True)

def get_batching_dict(args):
    return dict(
        max_tokens=args.batching_max_tokens
    )

def get_batcher(parser, args, model_interface):
    if args.batching_max_tokens is not None:
        return MaxTokensBatcher(
            args.batching_max_tokens,
            model_interface
        )
    else:
        raise ValueError

@dataclasses.dataclass
class Batcher:

    max_cost: int
    model_interface: SequenceToSequenceModelInterface

    def filter_pairs(self, data):
        return filter_pairs(data, self.is_small_enough)

    def generate_batches(self, data):
        return group_into_batches(data, self.is_small_enough)

    def generate_source_batches(self, data):
        return group_sources_into_batches(data, self.is_small_enough)

    def is_small_enough(self, batch_size, source_length, target_length):
        estimated_cost = self.estimate_cost(
            batch_size,
            self.model_interface.adjust_source_length(source_length),
            self.model_interface.adjust_target_length(target_length)
        )
        return estimated_cost <= self.max_cost

    def estimate_cost(self, batch_size, source_length, target_length):
        return batch_size * self.estimate_cost_single(source_length, target_length)

    def estimate_cost_single(self, source_length, target_length):
        raise NotImplementedError

@dataclasses.dataclass
class MaxTokensBatcher(Batcher):

    def filter_pairs(self, data):
        return data

    def estimate_cost_single(self, source_length, target_length):
        return max(source_length, target_length)
