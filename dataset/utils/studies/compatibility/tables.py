from typing import Sequence, Union

from pycldf import Source

from .enumerations import DefinedCompatibilityDataset

AB_INITIO_CLEANUP_TABLE: dict[str, str] = {
    "ă": "a",
    "ĕ": "e",
    "ĩ": "i",
    "ĭ": "i",
    "ó": "o",
    "ǒ": "o",
    "ŏ": "o",
    "ț": "t",
    "ú": "u",
    "ŭ": "u",
}

# Converts a long vowel represented either with a colon or a triangular colon to a macronized vowel.
PHONE_CONVERSION_TABLE: dict[str, str] = {
    "aː": "\u0101",
    "a:": "\u0101",
    "eː": "\u0113",
    "e:": "\u0113",
    "iː": "\u012B",
    "i:": "\u012B",
    "oː": "\u014D",
    "o:": "\u014D",
    "uː": "\u016B",
    "u:": "\u016B"
}

COLLATINUS_SECOND_DECLENSION_ENDINGS: Sequence[tuple[str, str]] = (
    ('um', '--s----a-'),
    ('i', '--s----g-'),
    ('o', '--s----d-'),
    ('o', '--s----b-'),
    ('i', '--p----n-'),
    ('i', '--p----v-'),
    ('os', '--p----a-'),
    ('orum', '--p----g-'),
    ('is', '--p----d-'),
    ('is', '--p----b-')
)

AB_ANTIQUO_SOURCE: Source = Source(
    genre="inproceedings",
    id_="meloniAntiquo2021",
    title="Ab Antiquo: {Neural} Proto-Language Reconstruction",
    booktitle="Proceedings of the 2021 {Conference} of the {North American Chapter} of the "
              "{Association} for {Computational Linguistics}: {Human Language Technologies}",
    author="Meloni, Carlo and Ravfogel, Shauli and Goldberg, Yoav",
    year="2021",
    month="jun",
    pages="4460--4473",
    publisher="Association for Computational Linguistics",
    address="Online",
    doi="10.18653/v1/2021.naacl-main.353"
)

OVERLAP_SOURCES: dict[str, Union[Source, list[Source]]] = {
    DefinedCompatibilityDataset.AB_ANTIQUO: AB_ANTIQUO_SOURCE,
    DefinedCompatibilityDataset.AB_INITIO: Source(
        genre="inproceedings",
        id_="ciobanuBuildingDataset2014",
        title="Building a Dataset of Multilingual Cognates for the {Romanian} Lexicon",
        booktitle="Proceedings of the Ninth International Conference on Language Resources and Evaluation ({LREC}'14)",
        author="{Ciobanu, Alina Maria and Dinu, Liviu}",
        year="2014",
        month="may",
        pages="{1038--1043}",
        publisher="{European Language Resources Association (ELRA)}",
        address="{Reykjavik, Iceland}",
    ),
    DefinedCompatibilityDataset.COMPREHENSIVE_ROMANCE: AB_ANTIQUO_SOURCE,
    DefinedCompatibilityDataset.COGLUST: Source(
        genre="inproceedings",
        id_="wuCreatingLargescaleMultilingual2018",
        title="Creating Large-Scale Multilingual Cognate Tables",
        booktitle="Proceedings of the Eleventh International Conference on Language Resources and Evaluation "
                  "({{LREC}} 2018)",
        author="Wu, Winston and Yarowsky, David",
        year="2018",
        month="may",
        publisher="{European Language Resources Association (ELRA)}",
        address="Miyazaki, Japan"
    ),
    DefinedCompatibilityDataset.COGNET: [
        Source(
            genre="inproceedings",
            id_="batsurenCogNet2019",
            title="{CogNet}: {A} Large-Scale Cognate Database",
            booktitle="Proceedings of the 57th Annual Meeting of the Association for Computational Linguistics",
            author="Batsuren, Khuyagbaatar and Bella, Gabor and Giunchiglia, Fausto",
            year="2019",
            month="jul",
            pages="3136--3145",
            publisher="Association for Computational Linguistics",
            address="Florence, Italy",
            doi="10.18653/v1/P19-1302"
        ),
        Source(
            genre="article",
            id_="batsurenCognateDatabase2022",
            author="Batsuren, Khuyagbaatar and Bella, G{\'a}bor and Giunchiglia, Fausto",
            year="2022",
            month="mar",
            journal="Language Resources and Evaluation",
            volume="56",
            number="1",
            pages="165--189",
            issn="1574-0218",
            doi="10.1007/s10579-021-09544-6",
        )
    ],
    DefinedCompatibilityDataset.IECOR: Source(
        genre="article",
        id_="heggartyLanguageTrees2023",
        author=r"{Heggarty, Paul and Anderson, Cormac and Scarborough, Matthew and King, Benedict and "
               r"Bouckaert, Remco and Jocz, Lechos{\l}aw and K{\"u}mmel, Martin Joachim and J{\"u}gel, Thomas "
               r"and Irslinger, Britta and Pooth, Roland and Liljegren, Henrik and Strand, Richard F. and "
               r"Haig, Geoffrey and Mac{\'a}k, Martin and Kim, Ronald I. and Anonby, Erik and Pronk, Tijmen and "
               r"Belyaev, Oleg and {Dewey-Findell}, Tonya Kim and Boutilier, Matthew and Freiberg, Cassandra and "
               r"Tegethoff, Robert and Serangeli, Matilde and Liosis, Nikos and Stro{\'n}ski, Krzysztof and "
               r"Schulte, Kim and Gupta, Ganesh Kumar and Haak, Wolfgang and Krause, Johannes and Atkinson, Quentin D. "
               r"and Greenhill, Simon J. and K{\"u}hnert, Denise and Gray, Russell D.}",
        year="2023",
        journal="Science",
        volume="381",
        number="6656",
        pages="eabg0818",
        publisher="American Association for the Advancement of Science",
        doi="10.1126/science.abg0818",
        urldate="2023-09-12"
    ),
    DefinedCompatibilityDataset.IELEX: Source(
        genre="misc",
        id_="dunnIELex2022",
        title="{evotext/ielex-data-and-tree}: {IELex} Data and Tree (2022/03/28)",
        author="Dunn, Michael and Tresoldi, Tiago",
        year="2022",
        month="mar",
        publisher="Zenodo",
        doi="10.5281/zenodo.5556800",
        version="r20211108"
    ),
    DefinedCompatibilityDataset.IELEX_UT: Source(
        genre="web",
        id_="lrcIELEX2024",
        title="Indo-European Lexicon: PIE Etyma and IE Reflexes",
        author="{Linguistics Research Center}, {The University of Texas at Austin}",
        year="2024",
        month="jan",
        day="4",
        type="Lexicon",
        url="https://lrc.la.utexas.edu/lex",
        langid="english"
    ),
    DefinedCompatibilityDataset.JAMBU: Source(
        genre="inproceedings",
        id_="aroraJambu2023",
        title="Jambu: {A} Historical Linguistic Database for {South Asian} Languages",
        booktitle="Proceedings of the 20th {SIGMORPHON} Workshop on "
                  "Computational Research in Phonetics, Phonology, and Morphology",
        author="Arora, Aryaman and Farris, Adam and Basu, Samopriya and Kolichala, Suresh",
        year="2023",
        month="jul",
        pages="68--77",
        publisher="Association for Computational Linguistics",
        address="Toronto, Canada",
        doi="10.18653/v1/2023.sigmorphon-1.8",
    ),
    DefinedCompatibilityDataset.LUO_ROMANCE: Source(
        genre="phdthesis",
        id_="luoSoundChange2021",
        title="Automatic Methods for Sound Change Discovery",
        year="2021",
        month="sep",
        urldate="2024-03-01",
        author="Luo, Jiaming",
        school="Massachusetts Institute of Technology",
        url="https://dspace.mit.edu/handle/1721.1/140021"
    )
}
