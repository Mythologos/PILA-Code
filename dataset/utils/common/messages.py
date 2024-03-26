from .constants import NamedEnum


class AnalyzerMessage(NamedEnum):
    SUBSETS: str = "a flag indicating whether source-based subsets of the data should have their statistics displayed"


class ConverterMessage(NamedEnum):
    INPUT_FILE: str = "path to file where the raw TSV data file is stored"
    OUTPUT_DIRECTORY: str = "path to directory where CLDF-formatted data will be saved"


class CompatibilityMessage(NamedEnum):
    DATASET: str = "a single dataset name to be checked against the examined dataset " \
                   "(the `metadata_filepath` argument) for forms in common"
    APPEND: str = "flag indicating whether to add indices of forms in common to an overlaps.csv file " \
                  "for the examined dataset (the `metadata_filepath` argument)"


class GeneralMessage(NamedEnum):
    METADATA_FILEPATH: str = "a path to the CLDF JSON metadata file to be studied"


class ProtoMessage(NamedEnum):
    DATASETS: str = "one or more dataset names which are to be examined for their quantities of etymon-reflex pairs"
    DISPLAY_MAXIMA: str = "flag indicating whether the pair of ancestor and descendant languages " \
                          "with the maximal number of pairs is computed and printed to the console"


class ScraperMessage(NamedEnum):
    FILTERS: str = "zero or more names of filters to apply to etymon-reflex pairs to divide up data"
    INPUT_FILEPATH: str = "filepath to file containing URLs to search for scrapable pages"
    OUTPUT_FILEPATH: str = "path to output file location for main data file"
