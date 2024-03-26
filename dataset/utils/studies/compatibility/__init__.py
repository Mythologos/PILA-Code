from .enumerations import DefinedCompatibilityDataset, STANDARD_FORM_DATASETS
from .helpers import append_overlaps, correct_collatinus_mistakes, convert_pila, create_header
from .loaders import CompatibilityLoader, load_ab_initio_data, load_ab_antiquo_data, \
    load_coglust_data, load_cognet_data, load_iecor_data, load_ielex_data, load_ielex_ut_data, load_jambu_data, \
    load_luo_romance_data
from .tables import COLLATINUS_SECOND_DECLENSION_ENDINGS, OVERLAP_SOURCES, PHONE_CONVERSION_TABLE

ROOT_FILEPATH: str = "data/studies/compatibility"

COMPATIBILITY_DATASET_FILEPATHS: dict[str, str] = {
    DefinedCompatibilityDataset.AB_INITIO:
        f"{ROOT_FILEPATH}/comprehensive-romance/ab-initio/LREC-2014-parallel-list.txt",
    DefinedCompatibilityDataset.AB_ANTIQUO:
        f"{ROOT_FILEPATH}/comprehensive-romance/ab-antiquo/romance-orthography.txt",
    DefinedCompatibilityDataset.COMPREHENSIVE_ROMANCE:
        f"{ROOT_FILEPATH}/comprehensive-romance/combined/all-ortho-no-diac.txt",
    DefinedCompatibilityDataset.COGLUST:
        f"{ROOT_FILEPATH}/coglust/romance.tsv",
    DefinedCompatibilityDataset.COGNET:
        f"{ROOT_FILEPATH}/cognet/CogNet-v2.0.tsv",
    DefinedCompatibilityDataset.IECOR:
        f"{ROOT_FILEPATH}/iecor/cldf/cldf-metadata.json",
    DefinedCompatibilityDataset.IELEX_UT:
        f"{ROOT_FILEPATH}/ielex-ut",
    DefinedCompatibilityDataset.JAMBU:
        f"{ROOT_FILEPATH}/jambu/Wordlist-metadata.json",
    DefinedCompatibilityDataset.LUO_ROMANCE:
        f"{ROOT_FILEPATH}/luo-romance/latin_cogs.tsv"
}

COMPATIBILITY_DATASET_LOADERS: dict[str, CompatibilityLoader] = {
    DefinedCompatibilityDataset.AB_INITIO: load_ab_initio_data,
    DefinedCompatibilityDataset.AB_ANTIQUO: load_ab_antiquo_data,
    DefinedCompatibilityDataset.COMPREHENSIVE_ROMANCE: load_ab_antiquo_data,
    DefinedCompatibilityDataset.COGLUST: load_coglust_data,
    DefinedCompatibilityDataset.COGNET: load_cognet_data,
    DefinedCompatibilityDataset.IECOR: load_iecor_data,
    DefinedCompatibilityDataset.IELEX: load_ielex_data,
    DefinedCompatibilityDataset.IELEX_UT: load_ielex_ut_data,
    DefinedCompatibilityDataset.JAMBU: load_jambu_data,
    DefinedCompatibilityDataset.LUO_ROMANCE: load_luo_romance_data
}
