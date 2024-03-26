from .enumerations import DefinedProtoDataset
from .helpers import display_dataset_results, display_maximum_results
from .loaders import load_iecor_tallies, load_ielex_ut_tallies, load_jambu_tallies, load_cldf_tallies, \
    load_cldf_form_table_tallies, load_proto_germanic_tallies, load_proto_slavic_tallies, \
    ProtoLoader, ProtoMapping


ROOT_FILEPATH: str = "dataset/data/studies/proto"

PROTO_DATASET_FILEPATHS: dict[str, str] = {
    DefinedProtoDataset.IECOR:
        f"{ROOT_FILEPATH}/cldf/cldf-metadata.json",
    DefinedProtoDataset.IELEX_UT:
        f"{ROOT_FILEPATH}/ielex-ut",
    DefinedProtoDataset.JAMBU:
        f"{ROOT_FILEPATH}/jambu/Wordlist-metadata.json",
    DefinedProtoDataset.PROTO_AZTECAN:
        f"{ROOT_FILEPATH}/proto-aztecan/cldf/cldf-metadata.json",
    DefinedProtoDataset.PROTO_BIZIC:
        f"{ROOT_FILEPATH}/proto-bizic/cldf/cldf-metadata.json",
    DefinedProtoDataset.PROTO_BURMISH:
        f"{ROOT_FILEPATH}/proto-burmish/cldf/cldf-metadata.json",
    DefinedProtoDataset.PROTO_BAI:
        f"{ROOT_FILEPATH}/proto-bai/cldf/cldf-metadata.json",
    DefinedProtoDataset.PROTO_GERMANIC:
        f"{ROOT_FILEPATH}/proto-germanic/proto_germanic_cogs.tsv",
    DefinedProtoDataset.PROTO_KAREN:
        f"{ROOT_FILEPATH}/proto-karen/cldf/cldf-metadata.json",
    DefinedProtoDataset.PROTO_LALO:
        f"{ROOT_FILEPATH}/proto-lalo/cldf/cldf-metadata.json",
    DefinedProtoDataset.PROTO_MICRONESIAN:
        f"{ROOT_FILEPATH}/proto-micronesian/cldf/cldf-metadata.json",
    DefinedProtoDataset.PROTO_NAHUATL_CORACHOL:
        f"{ROOT_FILEPATH}/proto-nahuatl-corachol/cldf/cldf-metadata.json",
    DefinedProtoDataset.PROTO_PURUS:
        f"{ROOT_FILEPATH}/proto-purus/cldf/cldf-metadata.json",
    DefinedProtoDataset.PROTO_SLAVIC:
        f"{ROOT_FILEPATH}/proto-slavic/slavic_all_IPA.tsv",
    DefinedProtoDataset.PROTO_TUKANOAN:
        f"{ROOT_FILEPATH}/proto-tukanoan/cldf/cldf-metadata.json"
}

PROTO_DATASET_LOADERS: dict[str, ProtoLoader] = {
    DefinedProtoDataset.IECOR: load_iecor_tallies,
    DefinedProtoDataset.IELEX_UT: load_ielex_ut_tallies,
    DefinedProtoDataset.JAMBU: load_jambu_tallies,
    DefinedProtoDataset.PROTO_AZTECAN: load_cldf_tallies,
    DefinedProtoDataset.PROTO_BAI: load_cldf_form_table_tallies,
    DefinedProtoDataset.PROTO_BIZIC: load_cldf_form_table_tallies,
    DefinedProtoDataset.PROTO_BURMISH: load_cldf_form_table_tallies,
    DefinedProtoDataset.PROTO_GERMANIC: load_proto_germanic_tallies,
    DefinedProtoDataset.PROTO_KAREN: load_cldf_tallies,
    DefinedProtoDataset.PROTO_LALO: load_cldf_tallies,
    DefinedProtoDataset.PROTO_MICRONESIAN: load_cldf_tallies,
    DefinedProtoDataset.PROTO_NAHUATL_CORACHOL: load_cldf_tallies,
    DefinedProtoDataset.PROTO_PURUS: load_cldf_tallies,
    DefinedProtoDataset.PROTO_SLAVIC: load_proto_slavic_tallies,
    DefinedProtoDataset.PROTO_TUKANOAN: load_cldf_tallies
}
