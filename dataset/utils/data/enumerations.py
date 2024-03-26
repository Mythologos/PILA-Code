from ..common import NamedEnum


class DefinedIrregularity(NamedEnum):
    ASSOCIATION: str = "Association"
    BORROWING: str = "Borrowing"
    MORPHOLOGY: str = "Morphology"
    PARADIGM_LEVELING: str = "Paradigm Leveling"
    PHONOLOGY: str = "Phonology"


class DefinedLanguage(NamedEnum):
    LATIN: str = "latin"
    PROTO_ITALIC: str = "proto-italic"


class DefinedSource(NamedEnum):
    DE_VAAN: str = "deVaan2008"
    RIX: str = "rixRapportiOnomastici1981"
    WATKINS: str = "watkinsEtymaEnniana1973"
    WIKTIONARY: str = "wiktionary2017"


class DefinedTag(NamedEnum):
    CASE: str = "Case"
    DEGREE: str = "Degree"
    GENDER: str = "Gender"
    INFLECTION_CLASS: str = "Inflection_Class"
    MOOD: str = "Mood"
    NUMBER: str = "Number"
    POS: str = "Part_of_Speech"
    PERSON: str = "Person"
    TENSE: str = "Tense"
    VOICE: str = "Voice"
