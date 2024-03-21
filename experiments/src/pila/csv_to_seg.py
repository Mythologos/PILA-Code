import argparse
import collections
import csv
import itertools
import pathlib
import random

import pycldf

from pila.random_split import randomly_split

def load_lexemes(dataset):
    forms_by_cognate_set_id = collections.OrderedDict()
    for cognate in dataset.objects('CognateTable'):
        forms_by_cognate_set_id.setdefault(cognate.data['Cognateset_ID'], []).append(cognate.form)
    cognate_sets_by_lemma_id = collections.OrderedDict()
    for form_list in forms_by_cognate_set_id.values():
        lemma_id = get_lemma_id_of_form_list(form_list)
        cognate_set = form_list_to_cognate_set(form_list)
        cognate_sets_by_lemma_id.setdefault(lemma_id, []).append(cognate_set)
    return cognate_sets_by_lemma_id.values()

VALID_LANGUAGES = {'Proto-Italic', 'Latin'}

def get_lemma_id_of_form_list(form_list):
    lemma_id = None
    for form in form_list:
        if form.language.data['Name'] == 'Latin':
            lemma_id = form.data['Lemma_ID']
    if lemma_id is None:
        raise ValueError
    if not all(
        # All Proto-Italic forms have a Lemma_ID of None.
        form.language.data['Name'] == 'Proto-Italic' and form.data['Lemma_ID'] is None
        or form.data['Lemma_ID'] == lemma_id
        for form in form_list
    ):
        raise ValueError
    return lemma_id

def form_list_to_cognate_set(form_list):
    forms_by_lang_id = collections.OrderedDict()
    for form in form_list:
        language = form.language.data['Name']
        if language not in VALID_LANGUAGES:
            raise ValueError
        forms_by_lang_id.setdefault(language, []).append(form.data['Segments'])
    return forms_by_lang_id['Proto-Italic'], forms_by_lang_id['Latin']

def get_splits(input_dir, generator):
    cldf_dataset = pycldf.Dataset.from_metadata(input_dir / 'Wordlist-metadata.json')
    lexemes = list(load_lexemes(cldf_dataset))
    return tuple(randomly_split(lexemes, [80, 10, 10], generator=generator))

def split_to_pairs(lexemes):
    for lexeme in lexemes:
        for cognate_set in lexeme:
            etymon_list, reflex_list = cognate_set
            for etymon in etymon_list:
                etymon_str = ' '.join(etymon)
                for reflex in reflex_list:
                    reflex_str = ' '.join(reflex)
                    yield etymon_str, reflex_str

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=pathlib.Path, required=True)
    parser.add_argument('--training-data-output', type=pathlib.Path, required=True)
    parser.add_argument('--validation-data-output', type=pathlib.Path, required=True)
    parser.add_argument('--test-data-output', type=pathlib.Path, required=True)
    parser.add_argument('--random-seed', type=int, required=True)
    args = parser.parse_args()

    split_names = ('train', 'valid', 'test')
    split_dirs = (args.training_data_output, args.validation_data_output, args.test_data_output)
    generator = random.Random(args.random_seed)
    splits = get_splits(args.input, generator=generator)
    for name, output_dir, split in zip(split_names, split_dirs, splits):
        etymon_file_path = output_dir / 'etyma.seg'
        reflex_file_path = output_dir / 'reflexes.seg'
        print(f'writing {etymon_file_path}')
        print(f'writing {reflex_file_path}')
        with etymon_file_path.open('w') as etymon_file, \
             reflex_file_path.open('w') as reflex_file:
            for etymon, reflex in split_to_pairs(split):
                print(etymon, file=etymon_file)
                print(reflex, file=reflex_file)

if __name__ == '__main__':
    main()
