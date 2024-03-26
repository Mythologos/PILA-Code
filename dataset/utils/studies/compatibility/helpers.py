from cltk.alphabet.lat import JVReplacer
from pycldf import Dataset, Source

from .constants import HEADER_TEMPLATE
from .enumerations import DefinedCompatibilityDataset, STANDARD_FORM_DATASETS
from .tables import COLLATINUS_SECOND_DECLENSION_ENDINGS, OVERLAP_SOURCES, PHONE_CONVERSION_TABLE
from ...data import CLDFEntry, CLDFTable, MatchList, OVERLAP_TABLE_COLUMNS, PhoneSequence, FormSets


def append_overlaps(pila_dataset: Dataset, pila_ids: list[str], other_ids: list[str], direct_matches: MatchList,
                    indirect_matches: MatchList, dataset: str):
    if pila_dataset.get("overlaps.csv") is None:
        overlap_rows: CLDFTable = []
        pila_dataset.add_table("overlaps.csv", *OVERLAP_TABLE_COLUMNS, primaryKey="ID")
        pila_dataset.add_foreign_key("overlaps.csv", "Form_ID", "forms.csv", "ID")
        current_row_count: int = 0
    else:
        overlap_rows: CLDFTable = list(pila_dataset.iter_rows("overlaps.csv"))
        current_row_count: int = len(list(pila_dataset.iter_rows("overlaps.csv")))

    sources: list[Source] = \
        [OVERLAP_SOURCES[dataset]] if isinstance(OVERLAP_SOURCES[dataset], Source) else OVERLAP_SOURCES[dataset]
    pila_dataset.add_sources(*sources)
    source_ids: list[str] = [source.id for source in sources]

    tables: dict[str, CLDFTable] = {"overlaps.csv": overlap_rows}
    for match_index, (other_key, pila_key) in enumerate(direct_matches, start=current_row_count):
        overlap_entry: CLDFEntry = {
            "ID": match_index,
            "Form_ID": pila_ids[pila_key],
            "Dataset": dataset,
            "Overlap_Type": "direct",
            "Other_Form_ID": other_ids[other_key],
            "Source": source_ids
        }
        overlap_rows.append(overlap_entry)

    current_row_count += len(direct_matches)
    for match_index, (other_key, pila_key) in enumerate(indirect_matches, start=current_row_count):
        overlap_entry: CLDFEntry = {
            "ID": match_index,
            "Form_ID": pila_ids[pila_key],
            "Dataset": dataset,
            "Overlap_Type": "indirect",
            "Other_Form_ID": other_ids[other_key],
            "Source": source_ids
        }
        overlap_rows.append(overlap_entry)

    pila_dataset.write(**tables)
    pila_dataset.validate()


def compose_base_forms(pila_latin_forms: list[PhoneSequence], keep_lengths: bool = True) -> list[str]:
    pila_revised_forms: list[str] = []
    for form in pila_latin_forms:
        revised_form: str = ""
        for phone_index, phone in enumerate(form):
            if phone == "\u014B":   # handling of eng
                next_phone = form[phone_index + 1]
                if next_phone == "n":
                    revised_form += "g"
                elif next_phone == "g":
                    revised_form += "n"
                else:
                    raise ValueError(f"Context with next phone <{next_phone}> for <{form}> not handled.")
            elif keep_lengths is True and phone in PHONE_CONVERSION_TABLE.keys():
                revised_form += PHONE_CONVERSION_TABLE[phone]
            else:
                revised_form += phone
        else:
            pila_revised_forms.append(revised_form)

    return pila_revised_forms


def convert_pila(pila_latin_forms: list[PhoneSequence], dataset: str) -> FormSets:
    if dataset in STANDARD_FORM_DATASETS:
        pila_revised_forms: list[str] = convert_to_standard_form(pila_latin_forms)
    elif dataset == DefinedCompatibilityDataset.AB_INITIO:
        pila_revised_forms: list[str] = convert_to_ab_initio(pila_latin_forms)
    elif dataset == DefinedCompatibilityDataset.IECOR:
        pila_revised_forms: list[str] = convert_to_iecor(pila_latin_forms)
    else:
        raise ValueError(f"The dataset <{dataset}> is not recognized by this function.")

    pila_form_sets: FormSets = [{form} for form in pila_revised_forms]
    return pila_form_sets


def convert_to_ab_initio(pila_latin_forms: list[PhoneSequence]) -> list[str]:
    pila_revised_forms: list[str] = compose_base_forms(pila_latin_forms, keep_lengths=False)
    return pila_revised_forms


def convert_to_iecor(pila_latin_forms: list[PhoneSequence]) -> list[str]:
    pila_revised_forms: list[str] = compose_base_forms(pila_latin_forms, keep_lengths=True)

    replacer: JVReplacer = JVReplacer()
    for form_index, form in enumerate(pila_revised_forms):
        pila_revised_forms[form_index] = replacer.replace(form)

    return pila_revised_forms


def convert_to_standard_form(pila_latin_forms: list[PhoneSequence]) -> list[str]:
    pila_revised_forms: list[str] = compose_base_forms(pila_latin_forms, keep_lengths=True)
    return pila_revised_forms


def correct_collatinus_mistakes(macronless_form: str, declined_forms: list[tuple[str, str]]) -> list[tuple[str, str]]:
    # Collatinus sometimes returns endings without forms. Incidentally, such forms can overlap with actual Latin words.
    # We correct for this here.
    revised_forms: list[tuple[str, str]] = []
    for declined_form in declined_forms:
        if declined_form in COLLATINUS_SECOND_DECLENSION_ENDINGS:
            form, tags = declined_form
            revised_form = macronless_form + form
            revised_forms.append((revised_form, tags))
        else:
            revised_forms.append(declined_form)
    return revised_forms


def create_header(dataset: str) -> str:
    return HEADER_TEMPLATE.format(dataset)
