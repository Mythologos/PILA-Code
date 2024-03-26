from statistics import mean, stdev

from ...data.enumerations import DefinedLanguage
from ...data.structures import CognateSets


def get_cognate_set_count(cognate_sets: CognateSets) -> int:
    return len(cognate_sets)


def get_word_count(cognate_sets: CognateSets, language: str) -> int:
    reflexes, etyma = zip(*cognate_sets)
    if language == DefinedLanguage.LATIN:
        word_count: int = sum([len(set_reflexes) for set_reflexes in reflexes])
    elif language == DefinedLanguage.PROTO_ITALIC:
        word_count: int = sum([len(set_etyma) for set_etyma in etyma])
    else:
        raise ValueError(f"The language <{language}> is not defined for this function.")
    return word_count


def get_phone_count(cognate_sets: CognateSets, language: str) -> int:
    reflexes, etyma = zip(*cognate_sets)
    if language == DefinedLanguage.LATIN:
        phone_count: int = sum([len(set_reflex) for set_reflexes in reflexes for set_reflex in set_reflexes])
    elif language == DefinedLanguage.PROTO_ITALIC:
        phone_count: int = sum([len(set_etymon) for set_etyma in etyma for set_etymon in set_etyma])
    else:
        raise ValueError(f"The language <{language}> is not defined for this function.")
    return phone_count


def get_pair_count(cognate_sets: CognateSets) -> int:
    pair_count: int = sum([len(set_reflexes) * len(set_etyma) for (set_reflexes, set_etyma) in cognate_sets])
    return pair_count


def get_phone_type_count(cognate_sets: CognateSets, language: str) -> int:
    reflexes, etyma = zip(*cognate_sets)
    if language == DefinedLanguage.LATIN:
        phone_type_count: int = \
            len(set([phone for set_reflexes in reflexes for set_reflex in set_reflexes for phone in set_reflex]))
    elif language == DefinedLanguage.PROTO_ITALIC:
        phone_type_count: int = \
            len(set([phone for set_etyma in etyma for set_etymon in set_etyma for phone in set_etymon]))
    elif language == "any":
        reflex_phone_types: set[str] = \
            set([phone for set_reflexes in reflexes for set_reflex in set_reflexes for phone in set_reflex])
        etymon_phone_types: set[str] = \
            set([phone for set_etyma in etyma for set_etymon in set_etyma for phone in set_etymon])
        all_phone_types = reflex_phone_types.union(etymon_phone_types)
        phone_type_count: int = len(all_phone_types)
    else:
        raise ValueError(f"The language <{language}> is not defined for this function.")
    return phone_type_count


def get_average_sequence_length(cognate_sets: CognateSets, language: str) -> tuple[float, float]:
    reflexes, etyma = zip(*cognate_sets)
    if language == DefinedLanguage.LATIN:
        phoneme_counts: list[int] = [len(set_reflex) for set_reflexes in reflexes for set_reflex in set_reflexes]
    elif language == DefinedLanguage.PROTO_ITALIC:
        phoneme_counts: list[int] = [len(set_etymon) for set_etyma in etyma for set_etymon in set_etyma]
    elif language == "any":
        reflex_phoneme_counts: list[int] = [len(set_reflex) for set_reflexes in reflexes for set_reflex in set_reflexes]
        etymon_phoneme_counts: list[int] = [len(set_etymon) for set_etyma in etyma for set_etymon in set_etyma]
        phoneme_counts: list[int] = [*reflex_phoneme_counts, *etymon_phoneme_counts]
    else:
        raise ValueError(f"The language <{language}> is not defined for this function.")

    average_phoneme_count: float = mean(phoneme_counts)
    phoneme_count_deviation: float = stdev(phoneme_counts)
    return average_phoneme_count, phoneme_count_deviation


def check_paired_measure_validity(*lists):
    for i in range(1, len(lists)):
        assert len(lists[i - 1]) == len(lists[i])
