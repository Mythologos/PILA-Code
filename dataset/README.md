# Dataset Setup and Analysis for "PILA: A Historical-Linguistic Dataset of Proto-Italic and Latin"

This repository contains the code for dataset creation and analyses in the paper
"PILA: A Historical-Linguistic Dataset of Proto-Italic and Latin"
(Bothwell *et al.*, 2024). 

## Directory Structure

This directory contains both a set of CLIs and a set of directories. We describe each in turn.

### Command Line Interfaces

We provide five command-line interfaces (CLIs) to permit simplified replication of the studies performed in our paper. 
Below, we provide brief descriptions of each CLI and present their interfaces. 
We start with the dataset creation interfaces before moving on to the three CLIs pertaining to studies in this work.

### Scraper (`scraper.py`)

In our work, this tool was used to scrape Wiktionary to gather our initial dataset.
This data is pooled from a variety of Wiktionary contributors who often consult standard Latin etymological texts.

```
>>> python dataset/scraper.py -h 
usage: scraper.py [-h] [--filters {FilterType.AFFIX,FilterType.RECONSTRUCTION} [{FilterType.AFFIX,FilterType.RECONSTRUCTION} ...]] [--output-filepath OUTPUT_FILEPATH]
                  input_filepath
scraper.py: error: the following arguments are required: input_filepath

(PILA) C:\Users\sbjr1\Code\Research\Computational Historical Linguistics\PILA-Code>python dataset/scraper.py -h
usage: scraper.py [-h] [--filters {FilterType.AFFIX,FilterType.RECONSTRUCTION} [{FilterType.AFFIX,FilterType.RECONSTRUCTION} ...]] [--input-filepath INPUT_FILEPATH]
                  [--output-filepath OUTPUT_FILEPATH]

options:
  -h, --help            show this help message and exit
  --filters {FilterType.AFFIX,FilterType.RECONSTRUCTION} [{FilterType.AFFIX,FilterType.RECONSTRUCTION} ...]
                        zero or more names of filters to apply to etymon-reflex pairs to divide up data
  --input-filepath INPUT_FILEPATH
                        filepath to file containing URLs to search for scrapable pages
  --output-filepath OUTPUT_FILEPATH
                        path to output file location for main data file
```

#### CLDF Converter (`cldf_converter.py`)

This CLI was used to convert the TSV file presented in `data/raw/tsv` to the CLDF format. 
It creates and fills all tables but `overlaps.csv`, as that table is generated from interactions with other datasets.
The `compatibility_checker.py` tool can create the `overlaps.csv` file to fully create the dataset. 
The `README.md` file accompanying PILA was automatically generated through PyCLDF's command line interface (Forkel, 2023), 
although its formatting was manually cleaned.

```
python cldf_converter.py -h
usage: cldf_converter.py [-h] [--output-directory OUTPUT_DIRECTORY] input_file   
                                                                                 
positional arguments:                                                            
  input_file            path to file where the raw TSV data file is stored       
                                                                                 
options:                                                                         
  -h, --help            show this help message and exit                          
  --output-directory OUTPUT_DIRECTORY                                            
                        path to directory where CLDF-formatted data will be saved
```

#### CLDF Analyzer (`cldf_analyzer.py`)

This CLI presents a set of statistics regarding the PILA dataset. 
Such statistics include the number of forms in both languages (Latin and Proto-Italic), 
the number of phone types in each language (and collectively),
and the average sequence lengths of forms in each language (and collectively).
Subsets of the data, based on indicated data sources, can also be examined.

```
>>> python cldf_analyzer.py -h
usage: cldf_analyzer.py [-h] [--metadata-filepath METADATA_FILEPATH] [--subsets | --no-subsets]                                           
                                                                                                                                          
options:                                                                                                                                  
  -h, --help            show this help message and exit                                                                                   
  --metadata-filepath METADATA_FILEPATH                                                                                                   
                        a path to the CLDF JSON metadata file to be studied                                                               
  --subsets, --no-subsets                                                                                                                 
                        a flag indicating whether source-based subsets of the data should have their statistics displayed (default: False)
```

#### Compatibility Checker (`compatibility_checker.py`)

This CLI can be used to determine the compatibility of a dataset with PILA, 
employing the algorithm described in Section 5.2.1 of our paper. 
It works with a variety of pre-existing cognate datasets which contain Latin.

The `--append` flag can be used to add indices of connecting Latin words to the `overlaps.csv` table. 
To replicate our `overlaps.csv` table exactly, append each dataset to this table 
in the order of the datasets in Table 9 of our paper.

For more information on what indices are employed to connect forms from PILA with other datasets, 
see the [PILA](https://github.com/Mythologos/PILA) repository.

Note that any dataset used with this tool must be first collected and placed in its designated directory. 
The filepaths in `utils/studies/compatibility/__init__.py` indicate the files or directories that the tool will search for.

```
>>> python compatibility_checker.py -h
usage: compatibility_checker.py [-h] [--append | --no-append] --dataset
                                {DefinedCompatibilityDataset.AB_ANTIQUO,DefinedCompatibilityDataset.AB_INITIO,DefinedCompatibilityDataset.COGLUST,DefinedCompatibilityDataset.COGNET,
                                DefinedCompatibilityDataset.COMPREHENSIVE_ROMANCE,DefinedCompatibilityDataset.IECOR,DefinedCompatibilityDataset.IELEX,DefinedCompatibilityDataset.IELEX_UT,
                                DefinedCompatibilityDataset.JAMBU,DefinedCompatibilityDataset.LUO_ROMANCE}
                                [--metadata-filepath METADATA_FILEPATH]

options:
  -h, --help            show this help message and exit
  --append, --no-append
                        flag indicating whether to add indices of forms in common to an overlaps.csv file for the examined dataset (the `metadata_filepath` argument) (default: False)
  --dataset {DefinedCompatibilityDataset.AB_ANTIQUO,DefinedCompatibilityDataset.AB_INITIO,DefinedCompatibilityDataset.COGLUST,DefinedCompatibilityDataset.COGNET,
  DefinedCompatibilityDataset.COMPREHENSIVE_ROMANCE,DefinedCompatibilityDataset.IECOR,DefinedCompatibilityDataset.IELEX,DefinedCompatibilityDataset.IELEX_UT,DefinedCompatibilityDataset.JAMBU,
  DefinedCompatibilityDataset.LUO_ROMANCE}
                        a single dataset name to be checked against the examined dataset (the `metadata_filepath` argument) for forms in common
  --metadata-filepath METADATA_FILEPATH
                        a path to the CLDF JSON metadata file to be studied

```

#### Proto-Language Studier (`proto_studier.py`)

This CLI is used to examine the variety of ancestor and descendant language pairs in datasets other than PILA. 
Its results were used to fill Table 3; in particular, the `---display-maxima` flag was used to show 
the pairing of languages with the maximal amount of etymon-reflex pairs. 
The tool can also be used to examine the variety of etymon-reflex pairs available in each dataset, 
as, to the authors' knowledge, all such pairs explicitly delineated by each dataset are tallied.

```
>>> python proto_studier.py -h
usage: proto_studier.py [-h]
                        [--datasets {DefinedProtoDataset.IECOR,DefinedProtoDataset.IELEX_UT,DefinedProtoDataset.JAMBU,DefinedProtoDataset.PROTO_AZTECAN,DefinedProtoDataset.PROTO_BAI,DefinedProtoDataset.PROTO_BIZIC,DefinedProtoDataset.PROTO_BURMISH,DefinedProtoDataset.PROTO_GERMANIC,DefinedProtoDataset.PROTO_KAREN,DefinedProtoDataset.PROTO_LALO,DefinedProtoDataset.PROTO_MICRONESIAN,DefinedProtoDataset.PROTO_NAHUATL_CORACHOL,DefinedProtoDataset.PROTO_PURUS,DefinedProtoDataset.PROTO_SLAVIC,DefinedProtoDataset.PROTO_TUKANOAN} 
                        [{DefinedProtoDataset.IECOR,DefinedProtoDataset.IELEX_UT,DefinedProtoDataset.JAMBU,DefinedProtoDataset.PROTO_AZTECAN,DefinedProtoDataset.PROTO_BAI,DefinedProtoDataset.PROTO_BIZIC,DefinedProtoDataset.PROTO_BURMISH,DefinedProtoDataset.PROTO_GERMANIC,DefinedProtoDataset.PROTO_KAREN,DefinedProtoDataset.PROTO_LALO,DefinedProtoDataset.PROTO_MICRONESIAN,DefinedProtoDataset.PROTO_NAHUATL_CORACHOL,DefinedProtoDataset.PROTO_PURUS,DefinedProtoDataset.PROTO_SLAVIC,DefinedProtoDataset.PROTO_TUKANOAN} ...]]
                        [--display-maxima | --no-display-maxima]

options:
  -h, --help            show this help message and exit
  --datasets {DefinedProtoDataset.IECOR,DefinedProtoDataset.IELEX_UT,DefinedProtoDataset.JAMBU,DefinedProtoDataset.PROTO_AZTECAN,DefinedProtoDataset.PROTO_BAI,
  DefinedProtoDataset.PROTO_BIZIC,DefinedProtoDataset.PROTO_BURMISH,DefinedProtoDataset.PROTO_GERMANIC,DefinedProtoDataset.PROTO_KAREN,DefinedProtoDataset.PROTO_LALO,
  DefinedProtoDataset.PROTO_MICRONESIAN,DefinedProtoDataset.PROTO_NAHUATL_CORACHOL,DefinedProtoDataset.PROTO_PURUS,DefinedProtoDataset.PROTO_SLAVIC,DefinedProtoDataset.PROTO_TUKANOAN} 
  [{DefinedProtoDataset.IECOR,DefinedProtoDataset.IELEX_UT,DefinedProtoDataset.JAMBU,DefinedProtoDataset.PROTO_AZTECAN,
  DefinedProtoDataset.PROTO_BAI,DefinedProtoDataset.PROTO_BIZIC,DefinedProtoDataset.PROTO_BURMISH,DefinedProtoDataset.PROTO_GERMANIC,
  DefinedProtoDataset.PROTO_KAREN,DefinedProtoDataset.PROTO_LALO,DefinedProtoDataset.PROTO_MICRONESIAN,DefinedProtoDataset.PROTO_NAHUATL_CORACHOL,
  DefinedProtoDataset.PROTO_PURUS,DefinedProtoDataset.PROTO_SLAVIC,DefinedProtoDataset.PROTO_TUKANOAN} ...]
                        one or more dataset names which are to be examined for their quantities of etymon-reflex pairs
  --display-maxima, --no-display-maxima
                        flag indicating whether the pair of ancestor and descendant languages with the maximal number of pairs is computed and printed to the console (default: False)
```

### Subdirectories

This directory contains the following subdirectories:
* `data`: This directory contains a variety of datasets and stages of dataset development.
    - The `cldf` subdirectory should, upon use of the `cldf_converter.py` file, contain the CLDF dataset generated from the TSV file in `raw`.
    - The `raw` subdirectory contains files pertaining to various stages of PILA's development. It has a few further subdirectories.
      - `scraping`: This directory holds data pertaining to the scrape of Wiktionary that occurred on February 15th, 2022. 
      It contains the URL inputted to `scraper.py` in `urls` as well as both the postprocessed original outputs of the scraper 
      and a placeholder directory for current outputs of `scraper.py`. Regarding the postprocessed outputs, 
      the main postprocessing step performed was to divide the `proto_italic_data_main.txt` file between that file 
      and the `proto_italic_data_partial.txt` file. Other files were not touched.
      - `tsv`: The original TSV file used to create the latest PILA dataset as of this repository's public release.
    - The `studies` subdirectory contains further subdirectories for two of the studies performed with this work: 
    one on dataset compatibility (`compatibility`) and one on proto-language etymon-reflex pairs (`proto`). 
    Each of these provide further subdirectories for the variety of datasets used in this study, 
    and each `.gitkeep` file lists what data was used in a given directory and from where it was retrieved.
* `utils`: This directory contains the code which the variety of CLIs pull from. 
    - The `common` subdirectory holds code which all other directories can take advantage of, 
    including various useful constants and helper functions.
    - The `data` subdirectory includes code meant for generating CLDF from PILA's original TSV file. 
    It also provides basic loading functionalities for reflexes and cognate sets.
    - The `studies` subdirectory provides three further subdirectories which are critical to the functionality of three CLIs.
    The `analysis` subdirectory supports the `cldf_analyzer.py`; 
    the `compatibility` subdirectory supports the `compatibility_checker.py`;
    and, finally, the `proto` subdirectory supports the `proto_studier.py`.

## Installation and Setup

To set up an environment for this code, please use the `pila.yml` file with Conda. 
For example, use the following command:

```
conda env create -n PILA --file pila.yml
```

The CLIs presented above can be used to run each of the tools provided. 

The data creation scripts (`scraper.py` and `cldf_converter.py`) can be run with the default settings to simulate the original work. 
Regarding the `scraper.py` script, one should not expect exactly the same results as the original paper: 
as the script scrapes from the current version of Wiktionary, edits to Wiktionary pages and indexing will cause results to differ.
Moreover, the queries used to search Wiktionary pages needed to be altered due to the use of new tags for various elements on Wiktionary pages.
(For example, Proto-Italic forms formerly received the class attribute `Latinx mention`; they are now labeled with `Latn mention`.)

Turning to the scripts used for our work's studies, 
the analysis script can also be run with the default settings once PILA has been created with `cldf_converter.py` 
(assuming that the output location is the default).
The `proto_studier.py` and `compatibility_checker.py` scripts require more effort to replicate, 
as the datasets stemming from each study need to be retrieved. 
In each of the subdirectories of `data/studies` pertaining to these scripts, 
`.gitkeep` files have been supplied which list the origin of the data. 
If a given dataset is publicly available, its relevant commit is listed to version the other dataset.
Once a dataset has been gathered, it can be specified in both scripts with an option. 

The results produced in Table 3 of our paper can be gathered by using the `--display-maxima` flag in `proto_studier.py`.
The `overlaps.csv` file can be created and added to PILA via the `compatibility_checker.py` script; 
the `--append` flag needs to be used with each dataset in turn.

Beyond specifying those values to replicate our work, the default values of each CLI should suffice.

## Citation

To cite this repository, please use the following paper's citation:

```bibtex
@inproceedings{bothwellPILA2024,
  title = {{{PILA}}: {{A}} Historical-Linguistic Dataset of {{Proto-Italic}} and {{Latin}}},
  booktitle = {Proceedings of the {{The}} 2024 {{Joint International Conference}} on {{Computational Linguistics}}, {{Language Resources}} and {{Evaluation}}},
  author = {Bothwell, Stephen and DuSell, Brian and Chiang, David and Krostenko, Brian},
  year = "2024",
  month = may,
  publisher = {European Language Resources Association},
  address = {Turin, Italy},
  abstract = {Computational historical linguistics seeks to systematically understand processes of sound change, including during periods at which little to no formal recording of language is attested. At the same time, few computational resources exist which deeply explore phonological and morphological connections between proto-languages and their descendants. This is particularly true for the family of Italic languages. To assist historical linguists in the study of Italic sound change, we introduce the Proto-Italic to Latin (PILA) dataset, which consists of roughly 3,000 pairs of forms from Proto-Italic and Latin. We provide a detailed description of how our dataset was created and organized. Then, we exhibit PILA's value in two ways. First, we present baseline results for PILA on a pair of traditional computational historical linguistics tasks. Second, we demonstrate PILA's capability for enhancing other historical-linguistic datasets through a dataset compatibility study.},
  langid = {english},
  annotation = {To appear.}
}
```

For other works cited above, see below:
```bibtex
@misc{forkelPycldfPythonLibrary,
  title = {Pycldf: {{A}} Python Library to Read and Write {{CLDF}} Datasets},
  shorttitle = {Pycldf},
  author = {Forkel, Robert},
  urldate = {2023-10-05},
  copyright = {Apache Software License},
  keywords = {linguistics}
}
```