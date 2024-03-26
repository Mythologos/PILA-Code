from re import findall
from typing import Sequence, Union

from .cldf import CLDFEntry, CLDFTable
from .constants import HEADWORD_NUMERATION, PHONETIC_LATIN_TOKENIZER, PHONETIC_PROTO_ITALIC_TOKENIZER
from .enumerations import DefinedIrregularity, DefinedLanguage, DefinedTag
from .structures import PILARawEntry
from .tables import BASE_SOURCES, LANGUAGES, MANUAL_TOKENIZATION_TABLE, TAGSETS


def build_tables(entries: list[PILARawEntry]) -> tuple[dict[str, CLDFTable], CLDFTable]:
    language_table: CLDFTable = [value for value in LANGUAGES.values()]
    source_table: CLDFTable = [value for value in BASE_SOURCES.values()]
    lemma_table, lemma_mapping = build_lemma_table(entries)
    gloss_table, gloss_mapping = build_gloss_table(entries)
    tags_table, tags_mapping = build_tags_table(entries)
    form_table, cognate_table = build_data_tables(entries, lemma_mapping, gloss_mapping, tags_mapping)

    tables: dict[str, CLDFTable] = {
        "CognateTable": cognate_table,
        "FormTable": form_table,
        "glosses.csv": gloss_table,
        "LanguageTable": language_table,
        "lemmata.csv": lemma_table,
        "tags.csv": tags_table
    }

    return tables, source_table


def build_data_tables(entries: list[PILARawEntry], lemma_mapping: dict[int, int], gloss_mapping: dict[int, int],
                      tags_mapping: dict[tuple[int, int], int]) -> tuple[CLDFTable, CLDFTable]:
    form_table: CLDFTable = []
    cognate_table: CLDFTable = []

    form_index: int = 0
    cognate_set_index: int = 0
    for entry_index, entry in enumerate(entries):
        updated_form_index = \
            add_forms(form_table, entry, lemma_mapping, gloss_mapping, tags_mapping, form_index, entry_index)
        cognate_set_index = add_cognates(cognate_table, entry, form_table, form_index, cognate_set_index)
        form_index = updated_form_index

    return form_table, cognate_table


def add_forms(form_table: CLDFTable, entry: PILARawEntry, lemma_mapping: dict[int, int],
              gloss_mapping: dict[int, int], tags_mapping: dict[tuple[int, int], int],
              form_index: int, entry_index: int) -> int:
    latin_reflexes: list[str] = [entry.base_reflex]
    if entry.inflected_reflex != "":
        latin_reflexes.append(entry.inflected_reflex)

    lemma_id: Union[int, str] = lemma_mapping[entry_index]
    gloss_id: Union[int, str] = gloss_mapping.get(entry_index, "")

    for reflex_index, latin_reflex in enumerate(latin_reflexes):
        cleaned_reflex: str = latin_reflex.strip(HEADWORD_NUMERATION).replace(":", "ː")
        if cleaned_reflex in MANUAL_TOKENIZATION_TABLE.keys():
            tokenized_reflex: list[str] = MANUAL_TOKENIZATION_TABLE[cleaned_reflex]
        else:
            tokenized_reflex: list[str] = findall(PHONETIC_LATIN_TOKENIZER, cleaned_reflex)
        latin_entry: CLDFEntry = {
            "ID": form_index,
            "Language_ID": LANGUAGES[DefinedLanguage.LATIN]["ID"],
            "Parameter_ID": entry_index,
            "Lemma_ID": lemma_id,
            "Gloss_ID": gloss_id,
            "Tag_ID": tags_mapping[(entry_index, reflex_index)],
            "Form": cleaned_reflex,
            "Segments": tokenized_reflex
        }
        form_index += 1
        form_table.append(latin_entry)

    proto_italic_etyma: list[str] = [*entry.base_etyma, *entry.inflected_etyma]
    for proto_italic_etymon in proto_italic_etyma:
        cleaned_etymon: str = proto_italic_etymon.replace(":", "ː")
        tokenized_etymon: list[str] = findall(PHONETIC_PROTO_ITALIC_TOKENIZER, cleaned_etymon)
        proto_italic_entry: CLDFEntry = {
            "ID": form_index,
            "Language_ID": LANGUAGES[DefinedLanguage.PROTO_ITALIC]["ID"],
            "Parameter_ID": entry_index,
            "Lemma_ID": "",
            "Gloss_ID": gloss_id,
            "Tag_ID": "",
            "Form": cleaned_etymon,
            "Segments": tokenized_etymon
        }
        form_index += 1
        form_table.append(proto_italic_entry)

    return form_index


def add_cognates(cognate_table: CLDFTable, raw_entry: PILARawEntry, form_table: CLDFTable,
                 form_starting_index: int, cognate_set_index: int) -> int:
    base_cldf_entries: list[CLDFEntry] = [form_table[form_starting_index]]
    inflected_cldf_entries: list[CLDFEntry] = []
    base_etyma_count: int = len(raw_entry.base_etyma)

    if raw_entry.inflected_reflex != "":
        base_etyma_start: int = form_starting_index + 2
        inflected_cldf_entries.append(form_table[form_starting_index + 1])
    else:
        base_etyma_start: int = form_starting_index + 1

    inflected_etyma_start: int = base_etyma_start + base_etyma_count
    base_etyma_entries: list[CLDFEntry] = form_table[base_etyma_start:inflected_etyma_start]
    base_cldf_entries.extend(base_etyma_entries)

    inflected_etyma_count: int = len(raw_entry.inflected_etyma)
    inflected_etyma_entries: list[CLDFEntry] = \
        form_table[inflected_etyma_start:inflected_etyma_start + inflected_etyma_count]
    inflected_cldf_entries.extend(inflected_etyma_entries)

    for cldf_entry in base_cldf_entries:
        add_cognate_entry(cognate_table, cldf_entry, raw_entry, cognate_set_index)

    if len(base_etyma_entries) > 0:
        cognate_set_index += 1

    for cldf_entry in inflected_cldf_entries:
        add_cognate_entry(cognate_table, cldf_entry, raw_entry, cognate_set_index)

    if len(inflected_etyma_entries) > 0:
        cognate_set_index += 1

    return cognate_set_index


def add_cognate_entry(cognate_table: CLDFTable, form_entry: CLDFEntry, raw_entry: PILARawEntry, cognate_set_index: int):
    new_cognate_entry: CLDFEntry = {
        "ID": len(cognate_table),
        "Form_ID": form_entry["ID"],
        "Cognateset_ID": cognate_set_index,
        "Source": [raw_entry.source]
    }
    cognate_table.append(new_cognate_entry)


def build_lemma_table(entries: list[PILARawEntry]) -> tuple[CLDFTable, dict[int, int]]:
    lemma_table: CLDFTable = []
    lemma_index_mapping: dict[str, int] = {}
    lemma_entry_mapping: dict[int, int] = {}

    for entry_index, entry in enumerate(entries):
        if entry.lemma not in lemma_index_mapping:
            lemma_index: int = len(lemma_table) + 1
            lemma_entry: CLDFEntry = {"ID": lemma_index, "Name": entry.lemma}
            lemma_table.append(lemma_entry)
            lemma_index_mapping[entry.lemma] = lemma_index
        else:
            lemma_index = lemma_index_mapping[entry.lemma]

        lemma_entry_mapping[entry_index] = lemma_index

    return lemma_table, lemma_entry_mapping


def build_gloss_table(entries: list[PILARawEntry]) -> tuple[CLDFTable, dict[int, int]]:
    gloss_table: CLDFTable = []
    gloss_mapping: dict[int, int] = {}

    gloss_index: int = 0
    for entry_index, entry in enumerate(entries):
        if len(entry.irregularities) == 0 and entry.gloss == "":
            continue
        else:
            gloss_entry: CLDFEntry = {"ID": gloss_index}
            for irregularity in DefinedIrregularity:
                gloss_entry[irregularity.title().replace(" ", "_")] = True \
                    if irregularity in entry.irregularities else False
            gloss_entry["Comment"] = entry.gloss
            gloss_entry["Source"] = [entry.gloss_source]
            gloss_table.append(gloss_entry)
            gloss_mapping[entry_index] = gloss_index
            gloss_index += 1

    return gloss_table, gloss_mapping


def build_tags_table(entries: list[PILARawEntry]) -> tuple[CLDFTable, dict[tuple[int, int], int]]:
    tags_table: CLDFTable = []
    tags_mapping: dict[tuple[int, int], int] = {}
    tags_tracker: dict[Sequence[tuple[str, str]], int] = {}

    tag_index: int = 0
    for entry_index, entry in enumerate(entries):
        reflexes: list[str] = [entry.base_reflex, entry.inflected_reflex]
        reflex_tags: list[list[str]] = [entry.base_tags, entry.inflected_tags]
        for reflex_number, reflex in enumerate(reflexes):
            if reflex != "":
                tag_entry: CLDFEntry = {
                    "ID": tag_index,
                    DefinedTag.POS: entry.pos,
                    DefinedTag.INFLECTION_CLASS: entry.inflection_class,
                    DefinedTag.CASE: "",
                    DefinedTag.DEGREE: "",
                    DefinedTag.GENDER: "",
                    DefinedTag.MOOD: "",
                    DefinedTag.NUMBER: "",
                    DefinedTag.PERSON: "",
                    DefinedTag.TENSE: "",
                    DefinedTag.VOICE: "",
                    "Comment": "",
                    "Source": ""
                }

                relevant_tags: list[str] = reflex_tags[reflex_number]
                validation_kwargs: dict[str, str] = unpack_tags(entry, relevant_tags)
                morphological_tags: dict[str, str] = validate_tags(**validation_kwargs)
                tag_entry.update(morphological_tags)

                tags_data: Sequence[tuple[str, str]] = tuple([item for item in tag_entry.items() if item[0] != "ID"])
                if tags_data in tags_tracker:
                    mapped_tag_index: int = tags_tracker[tags_data]
                else:
                    tags_table.append(tag_entry)
                    tags_tracker[tags_data] = tag_index
                    mapped_tag_index = tag_index
                    tag_index += 1

                tags_mapping[(entry_index, reflex_number)] = mapped_tag_index

    return tags_table, tags_mapping


def unpack_tags(entry: PILARawEntry, relevant_tags: list[str]) -> dict[str, str]:
    if entry.pos in ("Noun", "Numeral", "Pronoun"):
        if entry.pos == "Numeral" and entry.inflection_class == "":
            validation_kwargs: dict[str, str] = {}
        else:
            case, gender, number = relevant_tags
            validation_kwargs: dict[str, str] = {
                DefinedTag.CASE: case,
                DefinedTag.GENDER: gender,
                DefinedTag.NUMBER: number
            }
    elif entry.pos == "Adjective":
        case, gender, number, degree = relevant_tags
        validation_kwargs = {
            DefinedTag.CASE: case,
            DefinedTag.GENDER: gender,
            DefinedTag.NUMBER: number,
            DefinedTag.DEGREE: degree
        }
    elif entry.pos == "Determiner":
        if entry.inflection_class == "Special":
            validation_kwargs = {}
        else:
            case, gender, number, degree = relevant_tags
            validation_kwargs = {
                DefinedTag.CASE: case,
                DefinedTag.GENDER: gender,
                DefinedTag.NUMBER: number,
                DefinedTag.DEGREE: degree
            }

    elif entry.pos == "Verb":
        person, number, tense, voice, mood = relevant_tags
        validation_kwargs = {
            DefinedTag.PERSON: person,
            DefinedTag.NUMBER: number,
            DefinedTag.TENSE: tense,
            DefinedTag.VOICE: voice,
            DefinedTag.MOOD: mood
        }
    elif entry.pos == "Participle":
        tense, voice, case, gender, number, degree = relevant_tags
        validation_kwargs = {
            DefinedTag.TENSE: tense,
            DefinedTag.VOICE: voice,
            DefinedTag.CASE: case,
            DefinedTag.GENDER: gender,
            DefinedTag.NUMBER: number,
            DefinedTag.DEGREE: degree
        }
    elif entry.pos == "Adverb":
        validation_kwargs = {DefinedTag.DEGREE: relevant_tags[0]}
    elif entry.pos in ("Conjunction", "Interjection", "Preposition"):
        validation_kwargs = {}
    else:
        raise ValueError(f"The part-of-speech <{entry.pos}> is not handled.")

    return validation_kwargs


def validate_tags(**tagged_kwargs) -> dict[str, str]:
    validated_tags: dict[str, str] = {}
    for key, value in tagged_kwargs.items():
        if value in TAGSETS[key].keys():
            validated_tags[key] = TAGSETS[key][value]
        else:
            raise ValueError(f"The value <{value}> is not valid for <{key}>.")

    return validated_tags
