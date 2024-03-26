from argparse import Namespace

from pycldf import Dataset
from pycldf.util import DictTuple

from .tables import LANGUAGES
from .enumerations import DefinedLanguage
from .structures import CognateSet, CognateSets, MonolingualCognateList, PhoneSequence


def load_cognate_sets(dataset: Dataset, subset: str = "all") -> CognateSets:
    cognate_sets: CognateSets = []
    cognateset2form: dict[int, set[int]] = {}
    for row in dataset.objects("CognateTable"):
        if subset != "all" and row.cldf.source[0] != subset:
            continue
        else:
            cognateset_id: int = int(row.cldf.cognatesetReference)
            if cognateset2form.get(cognateset_id, None) is None:
                cognateset2form[cognateset_id] = set()

            form_id: int = int(row.cldf.formReference)
            cognateset2form[int(cognateset_id)].add(form_id)

    form_table: DictTuple = dataset.objects("FormTable")
    for set_id, form_ids in cognateset2form.items():
        reflexes: MonolingualCognateList = []
        etyma: MonolingualCognateList = []
        cognate_set: CognateSet = (reflexes, etyma)
        for form_id in form_ids:
            form_row: Namespace = form_table[form_id].cldf
            language_id: int = int(form_row.languageReference)
            if language_id == LANGUAGES[DefinedLanguage.LATIN]["ID"]:
                reflexes.append(form_row.segments)
            elif language_id == LANGUAGES[DefinedLanguage.PROTO_ITALIC]["ID"]:
                etyma.append(form_row.segments)
            else:
                raise ValueError(f"Language ID <{language_id}> not recognized.")
        else:
            if len(reflexes) == 0 or len(etyma) == 0:
                raise ValueError(f"There is not a valid pair between <{reflexes}> and <{etyma}>.")
            cognate_sets.append(cognate_set)

    return cognate_sets


def load_reflexes(dataset: Dataset) -> tuple[list[PhoneSequence], list[str]]:
    reflexes: list[PhoneSequence] = []
    reflex_ids: list[str] = []
    form_table: DictTuple = dataset.objects("FormTable")
    for form_row in form_table:
        language_id: int = int(form_row.cldf.languageReference)
        if language_id != LANGUAGES[DefinedLanguage.LATIN]["ID"]:
            continue
        else:
            reflexes.append(form_row.cldf.segments)
            reflex_ids.append(form_row.cldf.id)

    return reflexes, reflex_ids
