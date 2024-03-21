set -e
set -u
set -o pipefail

usage() {
  echo "Usage: $0 <data-dir>"
}

data_dir=${1-}
if ! shift 1; then
  usage >&2
  exit 1
fi

mkdir -p "$data_dir"/pila-{train,valid,test}
python pila/csv_to_seg.py \
  --input ../pila/cldf \
  --training-data-output "$data_dir"/pila-train \
  --validation-data-output "$data_dir"/pila-valid \
  --test-data-output "$data_dir"/pila-test \
  --random-seed 1234
