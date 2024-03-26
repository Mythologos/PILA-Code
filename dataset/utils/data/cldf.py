from typing import Any, Sequence, TypeAlias, Union

from pycldf import term_uri

from .enumerations import DefinedIrregularity, DefinedTag

CLDFEntry: TypeAlias = dict[str, Any]
CLDFTable: TypeAlias = list[CLDFEntry]

GLOSS_TABLE_COLUMNS: Sequence[Union[str, dict[str, Any]]] = (
    term_uri("id"),
    {
        "name": DefinedIrregularity.ASSOCIATION,
        "datatype": {
            "base": "boolean",
            "format": "True|False",
        },
        "required": True,
        "dc:extent": "singlevalued"
    },
    {
        "name": DefinedIrregularity.BORROWING,
        "datatype": {
            "base": "boolean",
            "format": "True|False",
        },
        "required": True,
        "dc:extent": "singlevalued"
    },
    {
        "name": DefinedIrregularity.MORPHOLOGY,
        "datatype": {
            "base": "boolean",
            "format": "True|False",
        },
        "required": True,
        "dc:extent": "singlevalued"
    },
    {
        "name": DefinedIrregularity.PARADIGM_LEVELING.replace(" ", "_"),
        "datatype": {
            "base": "boolean",
            "format": "True|False",
        },
        "required": True,
        "dc:extent": "singlevalued"
    },
    {
        "name": DefinedIrregularity.PHONOLOGY,
        "datatype": {
            "base": "boolean",
            "format": "True|False",
        },
        "required": True,
        "dc:extent": "singlevalued"
    },
    term_uri("comment"),
    term_uri("source")
)

LEMMA_TABLE_COLUMNS: Sequence[Union[str, dict[str, Any]]] = (
    term_uri("id"),
    term_uri("name")
)

OVERLAP_TABLE_COLUMNS: Sequence[Union[str, dict[str, Any]]] = (
    term_uri("id"),
    {
        "name": "Form_ID",
        "datatype": {
            "base": "string",
            "format": "[a-zA-Z0-9_\\-]+",
        },
        "propertyUrl": "http://cldf.clld.org/v1.0/terms.rdf#formReference",
        "required": True,
        "dc:extent": "singlevalued"
    },
    {
        "name": "Overlap_Type",
        "datatype": {
            "base": "string",
            "format": "direct|indirect"
        },
        "required": True,
        "dc:extent": "singlevalued"
    },
    {
        "name": "Dataset",
        "datatype": {
            "base": "string",
            "format": "[a-zA-Z0-9_\\-]+",
        },
        "required": True,
        "dc:extent": "singlevalued"
    },
    {
        "name": "Other_Form_ID",
        "datatype": {
            "base": "string",
            "format": "[a-zA-Z0-9_\\-:;]+",
        },
        "required": True,
        "dc:extent": "singlevalued"
    },
    term_uri("comment"),
    term_uri("source")
)

TAG_TABLE_COLUMNS: Sequence[str] = (
    term_uri("id"),
    *list(DefinedTag),
    term_uri("comment"),
    term_uri("source")
)

