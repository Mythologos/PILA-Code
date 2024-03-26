from typing import Sequence

from ...common import NamedEnum


class DefinedProtoDataset(NamedEnum):
    IECOR: str = "ie-cor"
    IELEX_UT: str = "ielex-ut"
    JAMBU: str = "jambu"
    PROTO_AZTECAN: str = "proto-aztecan"
    PROTO_BAI: str = "proto-bai"
    PROTO_BIZIC: str = "proto-bizic"
    PROTO_BURMISH: str = "proto-burmish"
    PROTO_GERMANIC: str = "proto-germanic"
    PROTO_KAREN: str = "proto-karen"
    PROTO_LALO: str = "proto-lalo"
    PROTO_MICRONESIAN: str = "proto-micronesian"
    PROTO_NAHUATL_CORACHOL: str = "proto-nahuatl-corachol"
    PROTO_PURUS: str = "proto-purus"
    PROTO_SLAVIC: str = "proto-slavic"
    PROTO_TUKANOAN: str = "proto-tukanoan"


DATASET_PROTOLANGUAGES: dict[str, Sequence[str]] = {
    DefinedProtoDataset.IECOR: (
        "Proto-Albanian",
        "Proto-Anatolian",
        "Proto-Baltic",
        "Proto-Balto-Slavic",
        "Proto-Brythonic",
        "Proto-Celtic",
        "Proto-Germanic",
        "Proto-Greek",
        "Proto-Indic",
        "Proto-Indo European",
        "Proto-Indo-European",
        "Proto-Indo-Iranian",
        "Proto-Indo-Iranic",
        "Proto-Insular-Celtic",
        "Proto-Iranic",
        "Proto-Italic",
        "Proto-Slavic",
        "Proto-Tocharian"
    ),
    DefinedProtoDataset.IELEX_UT: ("Proto-Indo-European",),
    DefinedProtoDataset.JAMBU: ('Indo-Aryan', 'PDr', 'PNur', 'Indo-ir', 'PMu'),
    DefinedProtoDataset.PROTO_AZTECAN: ("ProtoAztecan",),
    DefinedProtoDataset.PROTO_BAI: ("ProtoBai",),
    DefinedProtoDataset.PROTO_BIZIC: ("ProtoBizic",),
    DefinedProtoDataset.PROTO_BURMISH: ("ProtoBurmish",),
    DefinedProtoDataset.PROTO_GERMANIC: ("ProtoGermanic",),
    DefinedProtoDataset.PROTO_KAREN: ("ProtoKaren",),
    DefinedProtoDataset.PROTO_LALO: ("ProtoLalo",),
    DefinedProtoDataset.PROTO_MICRONESIAN: (
        "protopohnpeicchuukic",
        "protoeasternoceanic",
        "protopohnpeic",
        "protowesternmalayopolynesian",
        "protochuukic",
        "uraustronesisch",
        "preprotomicronesian",
        "protokimbe",
        "protonakanai",
        "protooceanic",
        "protowesternmicronesian",
        "protomicronesian",
        "protocentralmicronesian",
        "protowillaumez",
        "protomalayopolynesian",
        "protopolynesian",
        "protolakalai",
        "preprotooceanic",
        "protoaustronesian"
    ),
    DefinedProtoDataset.PROTO_NAHUATL_CORACHOL: (
        "ProtoCoracholNahua",
        "ProtoUtoAztecan",
        "ProtoSouthernAztecan",
        "ProtoNahua"
    ),
    DefinedProtoDataset.PROTO_PURUS: ("ProtoPurus",),
    DefinedProtoDataset.PROTO_SLAVIC: (),
    DefinedProtoDataset.PROTO_TUKANOAN: ("Prototucanoan",),
}
