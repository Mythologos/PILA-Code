from argparse import ArgumentParser, BooleanOptionalAction, Namespace
from os import path
from typing import Sequence

from pycldf import Dataset

from utils.common import AnalyzerMessage, DEFAULT_METADATA_FILEPATH, display_templatic_results, GeneralMessage
from utils.data import DefinedLanguage, DefinedSource
from utils.studies.analysis import get_cognate_set_count, get_pair_count, get_word_count, \
    get_phone_count, get_phone_type_count, get_average_sequence_length
from utils.data import CognateSets, load_cognate_sets


# Constants:
SOURCE_SUBSETS: Sequence[str] = (DefinedSource.WIKTIONARY, DefinedSource.DE_VAAN)


def compute_measures(cognate_sets: CognateSets) -> dict[str, int]:
    # noinspection PyDictCreation
    results: dict[str, int] = {
        "cognate_set_count": get_cognate_set_count(cognate_sets),
        "pair_count": get_pair_count(cognate_sets),
        "latin_word_count": get_word_count(cognate_sets, language=DefinedLanguage.LATIN),
        "proto_italic_word_count": get_word_count(cognate_sets, language=DefinedLanguage.PROTO_ITALIC),
        "latin_phone_count": get_phone_count(cognate_sets, language=DefinedLanguage.LATIN),
        "proto_italic_phone_count": get_phone_count(cognate_sets, language=DefinedLanguage.PROTO_ITALIC),
        "latin_phone_type_count": get_phone_type_count(cognate_sets, language=DefinedLanguage.LATIN),
        "proto_italic_phone_type_count": get_phone_type_count(cognate_sets, language=DefinedLanguage.PROTO_ITALIC),
        "any_phone_type_count": get_phone_type_count(cognate_sets, language="any")
    }

    results["latin_average_sequence_length"], results["latin_sequence_length_deviation"] = \
        get_average_sequence_length(cognate_sets, language=DefinedLanguage.LATIN)
    results["proto_italic_average_sequence_length"], results["proto_italic_sequence_length_deviation"] = \
        get_average_sequence_length(cognate_sets, language=DefinedLanguage.PROTO_ITALIC)
    results["any_average_sequence_length"], results["any_sequence_length_deviation"] = \
        get_average_sequence_length(cognate_sets, language="any")

    return results


if __name__ == "__main__":
    parser: ArgumentParser = ArgumentParser()
    parser.add_argument(
        "--metadata-filepath", type=str, default=DEFAULT_METADATA_FILEPATH, help=GeneralMessage.METADATA_FILEPATH
    )
    parser.add_argument("--subsets", action=BooleanOptionalAction, default=False, help=AnalyzerMessage.SUBSETS)
    args: Namespace = parser.parse_args()

    if path.isfile(args.metadata_filepath) is False:
        raise ValueError(f"The given filepath, <{args.metadata_filepath}>, is not a valid file.")
    else:
        cldf_dataset: Dataset = Dataset.from_metadata(args.metadata_filepath)

    print("Gathering subsets...")

    cldf_cognate_sets: CognateSets = load_cognate_sets(cldf_dataset)
    cldf_wiktionary_cognate_sets: CognateSets = load_cognate_sets(cldf_dataset, subset=DefinedSource.WIKTIONARY)
    cldf_devaan_cognate_sets: CognateSets = load_cognate_sets(cldf_dataset, subset=DefinedSource.DE_VAAN)
    cldf_pairs: list[tuple[CognateSets, str]] = [
        (cldf_cognate_sets, "all"),
        (cldf_wiktionary_cognate_sets, DefinedSource.WIKTIONARY),
        (cldf_devaan_cognate_sets, DefinedSource.DE_VAAN)
    ]

    for sets, subset_name in cldf_pairs:
        if (args.subsets is True and subset_name in SOURCE_SUBSETS) or subset_name == "all":
            print(f"Computing measures for subset <{subset_name}>...")
            sets_results: dict[str, int] = compute_measures(sets)
            print(f"Displaying measures for subset <{subset_name}>...")
            header: str = f"Displaying Results for {subset_name.title()}"
            display_templatic_results(sets_results, header)
