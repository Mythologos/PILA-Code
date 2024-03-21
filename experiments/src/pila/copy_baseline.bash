set -e
set -u
set -o pipefail

usage() {
  echo "Usage: $0 <dataset-dir>"
}

dataset_dir=${1-}
if ! shift 1; then
  usage >&2
  exit 1
fi

python pila/evaluate.py \
  --inputs "$dataset_dir"/source.seg \
  --hypotheses "$dataset_dir"/source.seg \
  --references "$dataset_dir"/target.seg \
  | python pila/format_eval.py
