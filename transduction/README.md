# Transduction Experiments for "PILA: A Historical-Linguistic Dataset of Proto-Italic and Latin"

This repository contains the code for the transduction-based experiments in the paper
"PILA: A Historical-Linguistic Dataset of Proto-Italic and Latin" (Bothwell *et al.*, 2024). 
Specifically, it performs the tasks of *reflex prediction* (from Proto-Italic to Latin) 
and *etymon reconstruction* (from Latin to Proto-Italic). 
It includes all the code necessary to reproduce the experiments, 
as well as a Docker image definition that can be used 
to replicate the software environment it was developed in.

## Directory Structure

This directory contains the following subdirectories:
* `data/`: Contains the preprocessed training, validation, and test splits of
  the PILA dataset used for the experiments.
* `predictions/`: Contains outputs predicted by the transformer models whose
  scores are reported for the Proto-Italic-to-Latin (forward) and
  Latin-to-Proto-Italic (backward) tasks.
* `experiments/`: Contains scripts for reproducing experiments and figures.
  Details below.
* `scripts/`: Contains helper scripts for setting up the software environment,
  building container images, running containers, installing Python packages,
  etc. Instructions for using these scripts are below.
* `src/`: Contains source code for all models, training routines, etc.
* `tests/`: Contains unit tests for the code under `src/`.

## Installation and Setup

To rerun our experiments, start by cloning this repository and the PILA dataset:

    $ git clone --recurse-submodules <repo-url>

In order to foster reproducibility, the code for this paper was developed and
run inside a [Docker](https://www.docker.com/) container defined in the file
[`Dockerfile-dev`](Dockerfile-dev). To run this code, you can build the
Docker image yourself and run it using Docker. Or, if you don't feel like
installing Docker, you can simply use `Dockerfile-dev` as a reference for
setting up the software environment on your own system. You can also build
an equivalent [Singularity](https://sylabs.io/docs/#singularity) image which
can be used on an HPC cluster, where it is likely that Docker is not available
but Singularity is.

In any case, it is highly recommended to run most experiments on a machine with
access to an NVIDIA GPU so that they finish within a reasonable amount of time.

### Using Docker

In order to use the Docker image, you must first
[install Docker](https://www.docker.com/get-started).
If you intend to run any experiments on a GPU, you must also ensure that your
NVIDIA driver is set up properly and install the
[NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html).

In order to automatically build the Docker image, start the container, and open
up a bash shell inside of it, run

    $ bash scripts/docker-shell.bash --build

After you have built the image once, there is no need to do so again, so
afterward you can simply run

    $ bash scripts/docker-shell.bash

By default, this script starts the container in GPU mode, which will fail if
you are not running on a machine with a GPU. If you only want to run things in
CPU mode, you can run

    $ bash scripts/docker-shell.bash --cpu

### Using Singularity

If you use a shared HPC cluster at your institution, it might not support
Docker, but there's a chance it does support Singularity, which is an
alternative container runtime that is more suitable for shared computing
environments.

In order to run the code in a Singularity container, you must first obtain the
Docker image and then convert it to a `.sif` (Singularity image) file on a
machine where you have root access (e.g. your personal computer or
workstation). This requires installing both Docker and
[Singularity](https://docs.sylabs.io/guides/latest/user-guide/quick_start.html)
on that machine. Assuming you have already built the Docker image according to
the instructions above, you can use the following to create the `.sif` file:

    $ bash scripts/build-singularity-image.bash

This will create the file `pila-experiments.sif`. It is normal for this to take
several minutes. Afterward, you can upload the `.sif` file to your HPC cluster
and use it there.

You can open a shell in the Singularity container using

    $ bash scripts/singularity-shell.bash

This will work on machines that do and do not have an NVIDIA GPU, although it
will output a warning if there is no GPU.

You can find a more general tutorial on Singularity
[here](https://github.com/bdusell/singularity-tutorial).

### Additional Setup

Whatever method you use to run the code (whether in a Docker container,
Singularity container, or no container), you must run this script once *inside
the container shell*):

    $ bash scripts/setup.bash

Specifically, this script installs the Python packages required by our code,
which will be stored in the local directory rather than system-wide. We use the
package manager [Poetry](https://python-poetry.org/) to manage Python packages.

## Running Code

All files under `src/` should be run using `poetry` so they have access to the
Python packages provided by the Poetry package manager. This means you should
either prefix all of your commands with `poetry run` or run `poetry shell`
beforehand to enter a shell with Poetry's virtualenv enabled all the time. You
should run both Python and Bash scripts with Poetry, because the Bash scripts
might call out to Python scripts. All Bash scripts under `src/` should be run
with `src/` as the current working directory.

All scripts under `scripts/` and `experiments/` should be run with the
top-level directory as the current working directory.

## Running Experiments

The [`experiments/pila`](experiments/pila) directory contains scripts for
reproducing the experiments and tables presented in the paper. Some of these
scripts are intended to be used to submit jobs to a computing cluster. They
should be run outside the container. You will need to edit the file
[`experiments/submit-job.bash`](experiments/submit-job.bash)
to tailor it to your specific computing cluster. Other scripts are for plotting
or printing tables and should be run inside the container.

An explanation of the scripts is below.

* `submit_split_data_job.bash`: Split the raw PILA dataset into training,
  validation, and test splits. For convenience, the splits are already
  included in this repository, so this does not need to be run.
* `submit_prepare_data_job.bash`: Preprocess the PILA data so that it can be
  read by the training code.
* `submit_train_and_eval_jobs.bash`: Train and evaluate transformers on the
  preprocessed PILA dataset.
* `print_table.bash`: Print the main table of results.
* `print_hyperparameter_table.bash`: Print the table of hyperparameters of the
  best models.

## Citation

To cite this repository, please use to the following paper's citation:

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
