from csv import reader
from typing import Sequence, Callable

from pycldf import Dataset
from pycldf.util import DictTuple

from .enumerations import DATASET_PROTOLANGUAGES, DefinedProtoDataset


ProtoMapping = dict[str, dict[str, int]]
ProtoLoader = Callable[[str, str], ProtoMapping]


def accumulate_pair_counts(pair_counts: dict[str, dict[str, int]], cognate2langs: dict[str, list[str]],
                           proto_languages: Sequence[str]):
    for languages in cognate2langs.values():
        etymon_languages: list[str] = []
        reflex_languages: list[str] = []
        for language in languages:
            if language in proto_languages:
                etymon_languages.append(language)
            else:
                reflex_languages.append(language)

        if len(etymon_languages) > 0 and len(reflex_languages) > 0:
            for etymon_language in etymon_languages:
                for reflex_language in reflex_languages:
                    if pair_counts[etymon_language].get(reflex_language, None) is None:
                        pair_counts[etymon_language][reflex_language] = 0
                    pair_counts[etymon_language][reflex_language] += 1
        else:
            for etymon_language in etymon_languages:
                if pair_counts["unmatched"].get(etymon_language, None) is None:
                    pair_counts["unmatched"][etymon_language] = 0
                pair_counts["unmatched"][etymon_language] += 1

            for reflex_language in reflex_languages:
                if pair_counts["unmatched"].get(reflex_language, None) is None:
                    pair_counts["unmatched"][reflex_language] = 0
                pair_counts["unmatched"][reflex_language] += 1


def load_cldf_tallies(cldf_filepath: str, dataset: str) -> ProtoMapping:
    pair_counts: ProtoMapping = {"unmatched": {}}
    cldf_dataset: Dataset = Dataset.from_metadata(cldf_filepath)

    proto_languages: Sequence[str] = DATASET_PROTOLANGUAGES[dataset]
    for proto_language in proto_languages:
        pair_counts[proto_language] = {}

    form_table: DictTuple = cldf_dataset.objects("FormTable")
    cognate_table: DictTuple = cldf_dataset.objects("CognateTable")

    cognate2langs: dict[str, list[str]] = {}
    for cognate_row in cognate_table:
        cognateset_id: str = cognate_row.cldf.cognatesetReference
        form_id: str = cognate_row.cldf.formReference
        lang_id: str = form_table[form_id].cldf.languageReference
        if cognate2langs.get(cognateset_id, None) is None:
            cognate2langs[cognateset_id] = []
        cognate2langs[cognateset_id].append(lang_id)

    accumulate_pair_counts(pair_counts, cognate2langs, proto_languages)
    return pair_counts


def load_cldf_form_table_tallies(cldf_filepath: str, dataset: str) -> ProtoMapping:
    pair_counts: ProtoMapping = {"unmatched": {}}
    cldf_dataset: Dataset = Dataset.from_metadata(cldf_filepath)

    proto_languages: Sequence[str] = DATASET_PROTOLANGUAGES[dataset]
    for proto_language in proto_languages:
        pair_counts[proto_language] = {}

    form_table: DictTuple = cldf_dataset.objects("FormTable")
    cognate2langs: dict[str, list[str]] = {}

    for form_row in form_table:
        if dataset == DefinedProtoDataset.PROTO_BAI:
            # The value seems to be embedded in the ID but not discretely represented in the dataset.
            # noinspection PyTestUnpassedFixture
            cognate_set_id: str = form_row.data["ID"].split("_")[-1]
        elif dataset == DefinedProtoDataset.PROTO_BIZIC:
            cognate_set_id: str = form_row.data["Cognacy"]
        elif dataset == DefinedProtoDataset.PROTO_BURMISH:
            cognate_set_id: str = form_row.data["Partial_Cognacy"]
        else:
            raise ValueError(f"Dataset <{dataset}> not recognized for this function.")

        language_id: str = form_row.cldf.languageReference
        if cognate2langs.get(cognate_set_id, None) is None:
            cognate2langs[cognate_set_id] = []
        cognate2langs[cognate_set_id].append(language_id)

    accumulate_pair_counts(pair_counts, cognate2langs, proto_languages)
    return pair_counts


def load_proto_slavic_tallies(tsv_filepath: str, dataset: str) -> ProtoMapping:
    pair_counts: ProtoMapping = {dataset: {}}
    with open(tsv_filepath, encoding="utf-8", mode="r") as tsv_file:
        for line in tsv_file:
            etymon, language_indicator, raw_reflex, ipa_reflex = line.strip().split("\t")
            if language_indicator not in pair_counts[dataset].keys():
                pair_counts[dataset][language_indicator] = 0
            pair_counts[dataset][language_indicator] += 1

    return pair_counts


def load_proto_germanic_tallies(tsv_filepath: str, dataset: str) -> ProtoMapping:
    pair_counts: ProtoMapping = {dataset: {}}
    with open(tsv_filepath, encoding="utf-8", mode="r") as tsv_file:
        for line_index, line in enumerate(tsv_file):
            if line_index == 0:
                continue
            else:
                _, language_indicator, *_ = line.strip().split("\t")
                if language_indicator not in pair_counts[dataset].keys():
                    pair_counts[dataset][language_indicator] = 0
                pair_counts[dataset][language_indicator] += 1

    return pair_counts


def load_ielex_ut_tallies(directory_filepath: str, dataset: str) -> ProtoMapping:
    pair_counts: ProtoMapping = {}

    proto_language: str = DATASET_PROTOLANGUAGES[dataset][-1]
    pair_counts[proto_language] = {}

    language_table: dict[str, str] = {}
    with open(f"{directory_filepath}/lex_language.csv", encoding="utf-8", mode="r") as languages_file:
        languages_reader = reader(languages_file)
        for line_index, line in enumerate(languages_reader):
            if line_index == 0:
                continue
            else:
                language_id, language_name, *_ = line
                language_table[language_id] = language_name

    reflex_table: dict[str, str] = {}
    with open(f"{directory_filepath}/lex_reflex.csv", encoding="utf-8", mode="r") as reflexes_file:
        reflexes_reader = reader(reflexes_file)
        for line_index, line in enumerate(reflexes_reader):
            if line_index == 0:
                continue
            else:
                reflex_id, reflex_language_id, *_ = line
                reflex_table[reflex_id] = reflex_language_id

    with open(f"{directory_filepath}/lex_etyma_reflex.csv", encoding="utf-8", mode="r") as linking_file:
        linking_reader = reader(linking_file)
        for line_index, line in enumerate(linking_reader):
            if line_index == 0:
                continue
            else:
                link_id, etymon_id, reflex_id, *_ = line
                if language_table[reflex_table[reflex_id]] not in pair_counts[proto_language]:
                    pair_counts[proto_language][language_table[reflex_table[reflex_id]]] = 0
                pair_counts[proto_language][language_table[reflex_table[reflex_id]]] += 1

    return pair_counts


def load_iecor_tallies(cldf_filepath: str, dataset: str) -> ProtoMapping:
    pair_counts: ProtoMapping = {"unmatched": {}}

    proto_languages: Sequence[str] = DATASET_PROTOLANGUAGES[dataset]
    for proto_language in proto_languages:
        pair_counts[proto_language] = {}

    cldf_dataset: Dataset = Dataset.from_metadata(cldf_filepath)
    cognateset_table: DictTuple = cldf_dataset.objects("CognatesetTable")
    cognate_table: DictTuple = cldf_dataset.objects("CognateTable")
    form_table: DictTuple = cldf_dataset.objects("FormTable")
    language_table: DictTuple = cldf_dataset.objects("LanguageTable")

    relevant_cognate_sets: list[str] = \
        [row.data["ID"] for row in cognateset_table if row.data["Root_Language"] in proto_languages]

    for cognate_row in cognate_table:
        cognateset_id: str = cognate_row.cldf.cognatesetReference
        if cognateset_id in relevant_cognate_sets:
            current_proto_language: str = cognateset_table[cognateset_id].data["Root_Language"]
            form_id: str = cognate_row.cldf.formReference
            lang_id: str = form_table[form_id].cldf.languageReference
            current_reflex_language: str = language_table[lang_id].data["Name"]
            if pair_counts[current_proto_language].get(current_reflex_language, None) is None:
                pair_counts[current_proto_language][current_reflex_language] = 0
            pair_counts[current_proto_language][current_reflex_language] += 1

    redundant_pairs: list[tuple[str, str]] = [
        ("Proto-Indo-European", "Proto-Indo European"),
        ("Proto-Indo-Iranic", "Proto-Indo-Iranian")
    ]
    for (main, other) in redundant_pairs:
        other_counts = pair_counts[other]
        for (reflex, count) in other_counts.items():
            pair_counts[main][reflex] += count
        del pair_counts[other]

    return pair_counts


def load_jambu_tallies(cldf_filepath: str, dataset: str) -> ProtoMapping:
    pair_counts: ProtoMapping = {"unmatched": {}}
    cldf_dataset: Dataset = Dataset.from_metadata(cldf_filepath)

    proto_languages: Sequence[str] = DATASET_PROTOLANGUAGES[dataset]
    for proto_language in proto_languages:
        pair_counts[proto_language] = {}

    form_table: DictTuple = cldf_dataset.objects("FormTable")
    parameter_table: DictTuple = cldf_dataset.objects("ParameterTable")
    relevant_cognate_sets: list[str] = []
    cognate2langs: dict[str, list[str]] = {}
    for parameter_row in parameter_table:
        # This corresponds with the listed DATASET_PROTOLANGUAGES, so there's no need to check it here.
        if parameter_row.data["Name"] is not None and parameter_row.data["Name"].startswith("*") is True:
            relevant_cognate_sets.append(parameter_row.data["ID"])
            cognate2langs[parameter_row.data["ID"]] = [parameter_row.data["Language_ID"]]

    for form_row in form_table:
        language_id: str = form_row.cldf.languageReference
        cognateset_id: str = form_row.cldf.parameterReference
        if language_id not in proto_languages and cognateset_id in relevant_cognate_sets:
            cognate2langs[cognateset_id].append(language_id)

    accumulate_pair_counts(pair_counts, cognate2langs, proto_languages)

    language_table: DictTuple = cldf_dataset.objects("LanguageTable")
    translated_pair_counts: dict[str, dict[str, int]] = {}
    for proto_language, reflex_languages in pair_counts.items():
        if proto_language != "unmatched":
            translated_proto_language: str = language_table[proto_language].data["Name"]
        else:
            translated_proto_language = proto_language

        translated_reflex_counts: dict[str, int] = {
            language_table[reflex_language].data["Name"]: count for reflex_language, count in reflex_languages.items()
        }
        translated_pair_counts[translated_proto_language] = translated_reflex_counts
    else:
        pair_counts = translated_pair_counts

    return pair_counts
