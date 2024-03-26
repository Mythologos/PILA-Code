from typing import Union

from pycldf import Source

from .enumerations import DefinedLanguage, DefinedSource, DefinedTag
from .cldf import CLDFEntry

BASE_SOURCES: dict[str, Union[Source]] = {
    DefinedSource.DE_VAAN: Source(
        genre="book",
        id_=DefinedSource.DE_VAAN.value,
        author="Michiel de Vaan",
        year="2008",
        title="Etymological Dictionary of Latin and the other Italic Languages",
        series="Leiden Indo-European Etymological Dictionary Series",
        number="7",
        publisher="Leiden",
        address="Leiden; Boston",
        isbn="978-90-04-16797-1",
        langid="english",
        keywords="Italic languages and dialects -- Etymology -- Dictionaries,Latin language -- Etymology -- "
                 "Dictionaries,Proto-Indo-European language -- Etymology -- Dictionaries"
    ),
    DefinedSource.RIX: Source(
        genre="incollection",
        id_=DefinedSource.RIX.value,
        author="Helmut Rix",
        editor="Colonna, G.",
        year="1981",
        pages="104-126",
        publisher="Giorgio Brettschneider",
        address="Rome",
        isbn="88-85007-51-1",
        langid="Italian"
    ),
    DefinedSource.WATKINS: Source(
        genre="article",
        id_="watkinsEtymaEnniana1973",
        title="Etyma {Enniana}",
        author="Calvert Watkins",
        year="1973",
        journal="{Harvard Studies in Classical Philology}",
        volume="77",
        pages="196-206",
        langid="English"
    ),
    DefinedSource.WIKTIONARY: Source(
        genre="misc",
        id_=DefinedSource.WIKTIONARY.value,
        author="{Wikipedia contributors}",
        year="2017",
        month="jul",
        title="Category:Latin terms derived from Proto-Italic",
        journal="Wiktionary, the free dictionary",
        urldate="2022-02-15",
        copyright="Creative Commons Attribution-ShareAlike License",
        langid="english",
        url="https://en.wiktionary.org/wiki/Category:Latin_terms_derived_from_Proto-Italic"
    ),
}

LANGUAGES: dict[str, CLDFEntry] = {
    DefinedLanguage.LATIN: {
        "ID": 1,
        "Name": "Latin",
        "Glottocode": "lati1261",
        "ISO639P3code": "lat",
        "Latitude": 41.90,
        "Longitude": 12.45
    },
    DefinedLanguage.PROTO_ITALIC: {
        "ID": 2,
        "Name": "Proto-Italic",
        "Glottocode": "ital1284",
    }
}

MANUAL_TOKENIZATION_TABLE: dict[str, list[str]] = {
    "ceu": ["c", "eu"],
    "cuiius": ["c", "ui", "i", "u", "s"],
    "quei": ["qu", "ei"]
}

TAGSETS: dict[str, dict[str, str]] = {
    DefinedTag.PERSON: {
        "1": "First",
        "2": "Second",
        "3": "Third"
    },
    DefinedTag.NUMBER: {
        "S": "Singular",
        "P": "Plural"
    },
    DefinedTag.TENSE: {
        "Pr": "Present",
        "Im": "Imperfect",
        "Ft": "Future",
        "Pf": "Perfect",
        "Pl": "Pluperfect",
        "Fp": "Future Perfect"
    },
    DefinedTag.MOOD: {
        "Ind": "Indicative",
        "Imp": "Imperative",
        "Sub": "Subjunctive",
        "Inf": "Infinitive"
    },
    DefinedTag.VOICE: {
        "Act": "Active",
        "Dep": "Deponent",
        "Psv": "Passive"
    },
    DefinedTag.GENDER: {
        "M": "Masculine",
        "F": "Feminine",
        "N": "Neuter",
        "M/F": "Masculine/Feminine",
        "M/N": "Masculine/Neuter",
        "F/N": "Feminine/Neuter",
        "M/F/N": "Any",
    },
    DefinedTag.CASE: {
        "Nm": "Nominative",
        "Gn": "Genitive",
        "Dt": "Dative",
        "Ac": "Accusative",
        "Ab": "Ablative",
        "Vc": "Vocative",
        "Lc": "Locative",
        "Any": "Any"
    },
    DefinedTag.DEGREE: {
        "Ps": "Positive",
        "Cm": "Comparative",
        "Sp": "Superlative"
    }
}
