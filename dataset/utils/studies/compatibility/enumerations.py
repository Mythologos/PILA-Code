from typing import Sequence

from ...common import NamedEnum


class DefinedCompatibilityDataset(NamedEnum):
    AB_ANTIQUO: str = "ab-antiquo"
    AB_INITIO: str = "ab-initio"
    COGLUST: str = "coglust"
    COGNET: str = "cognet"
    COMPREHENSIVE_ROMANCE: str = "comp-rom"
    IECOR: str = "ie-cor"
    IELEX: str = "ielex"
    IELEX_UT: str = "ielex-ut"
    JAMBU: str = "jambu"
    LUO_ROMANCE: str = "luo-romance"


STANDARD_FORM_DATASETS: Sequence[str] = (
    DefinedCompatibilityDataset.AB_ANTIQUO,
    DefinedCompatibilityDataset.COMPREHENSIVE_ROMANCE,
    DefinedCompatibilityDataset.COGLUST,
    DefinedCompatibilityDataset.COGNET,
    DefinedCompatibilityDataset.IELEX,
    DefinedCompatibilityDataset.IELEX_UT,
    DefinedCompatibilityDataset.JAMBU,
    DefinedCompatibilityDataset.LUO_ROMANCE
)
