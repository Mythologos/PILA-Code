import sys

import torch

def add_args(parser):
    parser.add_argument('--unk-string', default='<unk>')

def validate_args(parser, args):
    unk_string = args.unk_string
    if len(unk_string.split()) > 1:
        parser.error(f'unk string {unk_string!r} contains whitespace')

def get_token_types(tokens, unk_string):
    token_set = set(tokens)
    if unk_string is not None:
        has_unk = unk_string in token_set
        token_set.discard(unk_string)
    else:
        has_unk = False
    return token_set, has_unk

def get_token_types_in_file(path, unk_string):
    with path.open() as fin:
        return get_token_types(
            (token for line in fin for token in line.split()),
            unk_string
        )

def prepare_file(vocab, pair):
    input_path, output_path = pair
    print(f'preparing {input_path} => {output_path}', file=sys.stderr)
    with input_path.open() as fin:
        data = []
        for line_no, line in enumerate(fin, 1):
            try:
                data.append([vocab.to_int(token) for token in line.split()])
            except KeyError as e:
                raise ValueError(f'{input_path}:{line_no}: in line {line.rstrip()!r}: invalid token: {e}')
    torch.save(data, output_path)
