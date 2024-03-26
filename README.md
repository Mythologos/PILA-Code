# PILA: Applications and Studies

**Authors**: 
- Stephen Bothwell, David Chiang, Brian Krostenko (University of Notre Dame)
- Brian DuSell (ETH Zürich)

**Maintainer**: Stephen Bothwell

## Summary

This is a repository containing code for the LREC-COLING 2024 paper, 
**"PILA: A Historical-Linguistic Dataset of Proto-Italic and Latin."**
It contains relevant tools for public use. 

For the dataset that pertains to this paper, 
see the [PILA](https://github.com/Mythologos/PILA) repository.

## Contents

This repository contains two subdirectories which pertain to distinct studies performed in our paper. 
The `dataset` subdirectory contains CLI tools which allow for 
the scraping of Latin and Proto-Italic data from Wiktionary, 
the construction of PILA in CLDF from raw TSV data, 
the analysis of PILA with respect to various statistics, 
the examination of etymon-reflex pair quantities involving proto-languages across a variety of datasets,
and the performance of a dataset compatibility study.
Meanwhile, the `transduction` subdirectory permits the creation of a Docker environment 
to rerun the *reflex prediction* and *etymon reconstruction* performed on PILA in our work.

Note that each subdirectory has separate environment requirements. 
Both subdirectories contain further instructions as to the use of the tools within them.

## Contributing

This repository contains code relating to our LREC-COLING 2024 paper. 
The code was altered and cleaned before submission to promote usability, 
but it is possible that bugs were introduced in the interim. 
If you experience issues in using this code or request more instructions in reproducing our results,
please feel free to submit an issue regarding this.

We do not intend to heavily maintain this code, as it is meant to represent our paper at its time of publication. 
Exceptions may be made if warranted (*e.g.*, there is a bug which prevents the code from being correctly run), 
and we are happy to provide clarifications or assistance in reproducing our results. 

## Citations

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
