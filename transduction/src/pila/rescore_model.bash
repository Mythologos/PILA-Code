set -e
set -u
set -o pipefail

usage() {
  echo "$0 <data-dir> <train-dataset> <test-dataset> <model-dir> ..."
}

data_dir=${1-}
train_dataset=${2-}
test_dataset=${3-}
model_dir=${4-}
if ! shift 4; then
  usage >&2
  exit 1
fi
extra_args=("$@")

train_dir=$data_dir/$train_dataset
vocab_type=shared

result_dir=$model_dir/eval/$test_dataset
python pila/evaluate.py \
  --input "$data_dir"/"$test_dataset"/source.seg \
  --hypotheses "$result_dir"/translations.seg \
  --references "$train_dir"/datasets/"$test_dataset"/target.seg \
  | tee "$result_dir"/scores.json
