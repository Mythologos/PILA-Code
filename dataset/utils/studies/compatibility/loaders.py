from csv import reader
from json import loads
from re import findall, split, sub
from typing import Callable

from cltk.alphabet.lat import remove_accents, JVReplacer
from pycldf import Dataset

from .constants import IECOR_LATIN_ID, IELEX_UT_LANGUAGES, IELEX_UT_PATTERN, INITIO_PATTERN
from .tables import AB_INITIO_CLEANUP_TABLE, PHONE_CONVERSION_TABLE


CompatibilityLoader = Callable[[str], tuple[list[str], list[str]]]


def load_ab_antiquo_data(filepath: str) -> tuple[list[str], list[str]]:
    latin_forms: list[str] = []
    latin_form_ids: list[str] = []
    with open(filepath, encoding="utf-8", mode="r") as input_file:
        for line_index, line in enumerate(input_file):
            if line_index == 0:
                continue
            else:
                *_, latin_form = line.strip().split("\t")
                for (token, replacement) in PHONE_CONVERSION_TABLE.items():
                    latin_form = sub(token, replacement, latin_form)

                latin_forms.append(latin_form)
                latin_form_ids.append(str(line_index))

    return latin_forms, latin_form_ids


def load_ab_initio_data(filepath: str) -> tuple[list[str], list[str]]:
    latin_forms: list[str] = []
    latin_form_ids: list[str] = []
    with open(filepath, encoding="utf-8", mode="r") as input_file:
        for line_index, line in enumerate(input_file):
            if line_index < 2:
                continue
            else:
                *_, latin_form, _ = split(INITIO_PATTERN, line.strip())
                latin_form = latin_form.replace("-", "")
                latin_form = remove_accents(latin_form)
                for (token, replacement) in AB_INITIO_CLEANUP_TABLE.items():
                    latin_form = sub(token, replacement, latin_form)

                latin_forms.append(latin_form)
                latin_form_ids.append(str(line_index))

    return latin_forms, latin_form_ids


def load_coglust_data(filepath: str) -> tuple[list[str], list[str]]:
    latin_forms: list[str] = []
    latin_form_ids: list[str] = []

    with open(filepath, encoding="utf-8", mode="r") as input_file:
        for line_index, line in enumerate(input_file):
            items: list[str] = line.split("\t")
            for element_index, element in enumerate(items):
                if element.endswith("/lat") is True:
                    latin_forms.append(element.replace("/lat", ""))
                    latin_form_ids.append(f"{line_index}-{element_index}")

    return latin_forms, latin_form_ids


def load_cognet_data(filepath: str) -> tuple[list[str], list[str]]:
    latin_forms: list[str] = []
    latin_form_ids: list[str] = []
    with open(filepath, encoding="utf-8", mode="r") as input_file:
        seen_concepts: dict[str, list[str]] = {}
        for line_index, line in enumerate(input_file):
            if line_index < 1:
                continue
            else:
                concept_id, lang_1, word_1, lang_2, word_2, *_ = line.split("\t")
                pairs: list[tuple[str, str]] = [(lang_1, word_1), (lang_2, word_2)]
                for language, word in pairs:
                    if language == "lat":
                        if concept_id in seen_concepts.keys():
                            if word in seen_concepts[concept_id]:
                                continue
                            else:
                                latin_forms.append(word)
                                latin_form_ids.append(concept_id)
                                seen_concepts[concept_id].append(word)
                        else:
                            latin_forms.append(word)
                            latin_form_ids.append(concept_id)
                            seen_concepts[concept_id] = [word]
                    else:
                        continue

    return latin_forms, latin_form_ids


def load_iecor_data(filepath: str) -> tuple[list[str], list[str]]:
    latin_forms: list[str] = []
    latin_form_ids: list[str] = []
    iecor_dataset: Dataset = Dataset.from_metadata(filepath)
    for row in iecor_dataset.objects("FormTable"):
        if int(row.cldf.languageReference) == IECOR_LATIN_ID:
            latin_forms.append(row.cldf.form)
            latin_form_ids.append(row.cldf.id + "f")

    for row in iecor_dataset.objects("CognatesetTable"):
        if row.data["Root_Language"] == "Latin" and row.data["Root_Form"] not in latin_forms:
            latin_forms.append(row.data["Root_Form"])
            latin_form_ids.append(row.cldf.id + "cs")

    replacer: JVReplacer = JVReplacer()
    for form_index, form in enumerate(latin_forms):
        replaced_form: str = replacer.replace(form)
        latin_forms[form_index] = replaced_form

    return latin_forms, latin_form_ids


def load_ielex_data(filepath: str) -> tuple[list[str], list[str]]:
    latin_forms: list[str] = []
    latin_form_ids: list[str] = []
    with open(filepath, encoding="utf-8", mode="r") as input_file:
        for line in input_file:
            concept_alias, concept_id, language, lexeme, lexeme_id, *_ = line.strip().split("\t")
            if language != "Latin":
                continue
            else:
                latin_forms.append(lexeme)
                latin_form_ids.append(lexeme_id)

    for form_index, form in enumerate(latin_forms):
        replacement_pairs: list[tuple[str, str]] = [
            ("kw", "qu"), ("kʷ", "qu"), ("k", "c"), ("w", "v"), ("ˈ", ""), (".", ""), ("ɡ", "g"),
            ("ɪ", "i"), ("ɛ", "e"), ("ʊ", "u"), ("ɔ", "o"), ("cs", "x"), ("j", "i"), ("̄", "ː")
        ]
        for (token, replacement) in replacement_pairs:
            form = form.replace(token, replacement)

        if "\u014B" in form:
            next_phone = form[form.index("\u014B") + 1]
            if next_phone == "n":
                form = form.replace("\u014B", "g")
            elif next_phone == "g":
                form = form.replace("\u014B", "n")
            else:
                raise ValueError(f"Context with next phone <{next_phone}> for <{form}> not handled.")

        for token, replacement in PHONE_CONVERSION_TABLE.items():
            form = sub(token, replacement, form)

        latin_forms[form_index] = form

    return latin_forms, latin_form_ids


def load_jambu_data(filepath: str) -> tuple[list[str], list[str]]:
    latin_forms: list[str] = []
    latin_form_ids: list[str] = []

    jambu_dataset: Dataset = Dataset.from_metadata(filepath)
    for row in jambu_dataset.objects("FormTable"):
        if row.cldf.languageReference == "Lat":
            latin_forms.append(row.cldf.form)
            latin_form_ids.append(row.cldf.id)

    return latin_forms, latin_form_ids


def load_ielex_ut_data(directory_path: str) -> tuple[list[str], list[str]]:
    latin_forms: list[str] = []
    latin_form_ids: list[str] = []

    language_ids: list[str] = []
    with open(f"{directory_path}/lex_language.csv", encoding="utf-8", mode="r") as languages_file:
        languages_reader = reader(languages_file)
        for line_index, line in enumerate(languages_reader):
            line_language_id, line_language_name, *_ = line
            if line_index == 0:
                continue
            else:
                if line_language_name in IELEX_UT_LANGUAGES:
                    language_ids.append(line_language_id)

    if len(language_ids) == 0:
        raise ValueError(f"No language ID found for keys <{IELEX_UT_LANGUAGES}>.")

    with open(f"{directory_path}/lex_reflex.csv", encoding="utf-8", mode="r") as reflexes_file:
        reflexes_reader = reader(reflexes_file)
        for line_index, line in enumerate(reflexes_reader):
            line_reflex_id, line_language_id, *_, line_entry, line_extra = line
            if line_index == 0:
                continue
            elif line_language_id in language_ids:
                # All entries are lists of dictionaries containing key-value pairs.
                # The key is "text" and the value is the actual reflex in unicode.
                # We create a list through .strip() and .split(), even if there's only one element,
                #   and we use JSON's loads() to create a dictionary from each individual dictionary string.

                # noinspection PyTestUnpassedFixture
                reformatted_line_entry: list[str] = line_entry.strip("[]").split(",")
                reformatted_line_entry: list[dict[str, str]] = [loads(entry) for entry in reformatted_line_entry]
                for entry in reformatted_line_entry:
                    entry_text: str = entry["text"]
                    parenthetical_matches: list[str] = findall(IELEX_UT_PATTERN, entry_text)
                    new_forms: list[str] = []
                    if len(parenthetical_matches) == 1:
                        inclusive_form: str = entry_text.replace("(", "").replace(")", "")
                        exclusive_form: str = entry_text.replace(parenthetical_matches[-1], "")
                        new_forms.append(inclusive_form)
                        new_forms.append(exclusive_form)
                    elif len(parenthetical_matches) == 0:
                        new_forms.append(entry_text)
                    else:
                        raise ValueError(f"Number of matches, <{len(parenthetical_matches)}>, "
                                         f"exceeds handled number, for <{entry_text}>.")

                    for form in new_forms:
                        latin_forms.append(form)
                        latin_form_ids.append(line_reflex_id)

    return latin_forms, latin_form_ids


def load_luo_romance_data(filepath: str) -> tuple[list[str], list[str]]:
    # Since entries for each (or, at least, the vast majority of) etyma are for etyma that have already appeared,
    #   we collect a line-based mapping to get indices while representing all etyma only once.
    latin_form_mapping: dict[str, list[int]] = {}
    with open(filepath, encoding="utf-8", mode="r") as tsv_file:
        for line_index, line in enumerate(tsv_file, start=-1):
            if line_index == -1:
                continue
            else:
                etymon, *_ = line.strip().split("\t")
                if etymon not in latin_form_mapping:
                    latin_form_mapping[etymon] = []
                latin_form_mapping[etymon].append(line_index)

    latin_forms: list[str] = []
    latin_form_ids: list[str] = []
    for key, value in latin_form_mapping.items():
        latin_forms.append(key)
        latin_form_id: str = ";".join([str(index) for index in value])
        latin_form_ids.append(latin_form_id)

    return latin_forms, latin_form_ids
