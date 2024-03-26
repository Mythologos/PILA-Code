from argparse import ArgumentParser, BooleanOptionalAction, Namespace
from os import path
from typing import Callable

from cltk.morphology.lat import CLTKException, CollatinusDecliner
from cltk.alphabet.lat import remove_macrons
from numpy import uint16, zeros
from numpy.typing import NDArray
from scipy.optimize import linear_sum_assignment
from pycldf import Dataset

from utils.common import CompatibilityMessage, DEFAULT_METADATA_FILEPATH, display_templatic_results, \
    GeneralMessage
from utils.data import FormSets, MatchList, load_reflexes
from utils.studies.compatibility import COMPATIBILITY_DATASET_FILEPATHS, COMPATIBILITY_DATASET_LOADERS, \
    DefinedCompatibilityDataset, append_overlaps, correct_collatinus_mistakes, convert_pila, create_header


def compute_dataset_overlap(pila_form_sets: FormSets, other_form_sets: FormSets) -> \
        tuple[dict[str, float], MatchList, MatchList]:
    results: dict[str, float] = {"pila_size": len(pila_form_sets), "other_size": len(other_form_sets)}
    direct_matches: MatchList = compute_direct_overlap(pila_form_sets, other_form_sets, results)

    revised_pila_sets, revised_other_sets = remove_matched_sets(pila_form_sets, other_form_sets, direct_matches)
    assert len(direct_matches) == results["direct_overlap"]

    indirect_matches: MatchList = compute_indirect_overlap(revised_pila_sets, revised_other_sets, results)
    assert len(indirect_matches) == results["indirect_overlap"]
    results["pila_indirect_overlap_percentage"] = results["indirect_overlap"] / len(pila_form_sets)
    results["other_indirect_overlap_percentage"] = results["indirect_overlap"] / len(other_form_sets)

    results["total_overlap"] = results["direct_overlap"] + results["indirect_overlap"]
    results["pila_total_overlap_percentage"] = results["total_overlap"] / len(pila_form_sets)
    results["other_total_overlap_percentage"] = results["total_overlap"] / len(other_form_sets)
    assert len(indirect_matches) + len(direct_matches) == results["total_overlap"]

    return results, direct_matches, indirect_matches


def compute_direct_overlap(pila_form_sets: FormSets, other_form_sets: FormSets,
                           results: dict[str, float]) -> MatchList:
    results["direct_overlap"], direct_overlap_matches = compute_best_matching(pila_form_sets, other_form_sets)
    results["pila_direct_overlap_percentage"] = results["direct_overlap"] / len(pila_form_sets)
    results["other_direct_overlap_percentage"] = results["direct_overlap"] / len(other_form_sets)
    return direct_overlap_matches


def remove_matched_sets(pila_form_sets: FormSets, other_form_sets: FormSets,
                        matched_entries: MatchList) -> tuple[FormSets, FormSets]:
    revised_pila_form_sets: list[set[str]] = []
    revised_other_form_sets: list[set[str]] = []

    rows, columns = zip(*matched_entries)
    for item_index, form_set in enumerate(other_form_sets):
        if item_index not in rows:
            revised_other_form_sets.append(form_set)
        else:
            revised_other_form_sets.append(set())

    for item_index, form_set in enumerate(pila_form_sets):
        if item_index not in columns:
            revised_pila_form_sets.append(form_set)
        else:
            revised_pila_form_sets.append(set())

    return revised_pila_form_sets, revised_other_form_sets


def compute_indirect_overlap(pila_form_sets: FormSets, other_form_sets: FormSets,
                             results: dict[str, float]) -> MatchList:
    # We compute a more "approximate" measure of overlap by using Collatinus.
    # All datasets have some form of representation which is different from our use of traditional headwords.

    decliner: CollatinusDecliner = CollatinusDecliner()
    for form_set in pila_form_sets:
        if len(form_set) == 0:
            continue
        else:
            assert len(form_set) == 1
            macronless_form: str = remove_macrons(list(form_set)[-1])
            form_set.add(macronless_form)
            try:
                declined_forms: list[tuple[str, str]] = decliner.decline(macronless_form)
                revised_declined_forms: list[tuple[str, str]] = \
                    correct_collatinus_mistakes(macronless_form, declined_forms)
                for (declined_form, _) in revised_declined_forms:
                    if declined_form != "":
                        form_set.add(declined_form)
            except (CLTKException, KeyError):
                pass

    for form_set in other_form_sets:
        if len(form_set) == 0:
            continue
        else:
            assert len(form_set) == 1
            macronless_form: str = remove_macrons(list(form_set)[-1])
            form_set.add(macronless_form)

    indirect_overlap, indirect_overlap_matches = compute_best_matching(pila_form_sets, other_form_sets)
    results["indirect_overlap"] = indirect_overlap

    return indirect_overlap_matches


def compute_best_matching(pila_form_sets: list[set[str]], other_form_sets: list[set[str]]) -> tuple[int, MatchList]:
    max_length: int = max(len(pila_form_sets), len(other_form_sets))
    score_matrix: NDArray[uint16] = zeros((max_length, max_length), dtype=uint16)
    for form_index, other_form_set in enumerate(other_form_sets):
        for form_set_index, pila_form_set in enumerate(pila_form_sets):
            score_matrix[form_index, form_set_index] = 1 if len(other_form_set.intersection(pila_form_set)) > 0 else 0

    rows, columns = linear_sum_assignment(score_matrix, maximize=True)   # type: ignore
    lsa_entries: list[tuple[int, int]] = list(zip(rows, columns))
    scoring_lsa_entries: MatchList = []
    best_matching_score: int = 0
    for (row, column) in lsa_entries:
        best_matching_score += score_matrix[row, column].item()
        if score_matrix[row, column].item() == 1:
            scoring_lsa_entries.append((row, column))

    return best_matching_score, scoring_lsa_entries


if __name__ == "__main__":
    parser: ArgumentParser = ArgumentParser()
    parser.add_argument("--append", action=BooleanOptionalAction, default=False, help=CompatibilityMessage.APPEND)
    parser.add_argument(
        "--dataset", type=str, choices=list(DefinedCompatibilityDataset), required=True,
        help=CompatibilityMessage.DATASET
    )
    parser.add_argument(
        "--metadata-filepath", type=str, default=DEFAULT_METADATA_FILEPATH, help=GeneralMessage.METADATA_FILEPATH
    )
    args: Namespace = parser.parse_args()

    if path.isfile(args.metadata_filepath) is False:
        raise ValueError(f"The given filepath, <{args.metadata_filepath}>, is not a valid file.")
    else:
        cldf_dataset: Dataset = Dataset.from_metadata(args.metadata_filepath)
        pila_reflexes, pila_reflex_ids = load_reflexes(cldf_dataset)
        pila_latin_sets: FormSets = convert_pila(pila_reflexes, args.dataset)

    dataset_filepath: str = COMPATIBILITY_DATASET_FILEPATHS[args.dataset]
    dataset_loader: Callable[[str], tuple[list[str], list[str]]] = COMPATIBILITY_DATASET_LOADERS[args.dataset]
    dataset_latin_forms, dataset_latin_ids = dataset_loader(dataset_filepath)
    dataset_latin_sets: FormSets = [{form} for form in dataset_latin_forms]
    overlap_results, direct_list, indirect_list = compute_dataset_overlap(pila_latin_sets, dataset_latin_sets)

    header: str = create_header(args.dataset)
    display_templatic_results(overlap_results, header)

    if args.append is True:
        assert len(pila_reflex_ids) == len(pila_latin_sets)
        assert len(dataset_latin_ids) == len(dataset_latin_sets)
        append_overlaps(cldf_dataset, pila_reflex_ids, dataset_latin_ids, direct_list, indirect_list, args.dataset)
