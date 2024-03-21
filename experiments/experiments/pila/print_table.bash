set -e
set -u
set -o pipefail

. "$(dirname "$BASH_SOURCE")"/include.bash

cd "$ROOT_DIR"/src

for direction in forward backward; do
  echo "direction: $direction"
  echo "copy baseline:"
  bash pila/copy_baseline.bash "$PILA_DATA_DIR"/pila-"$direction"-train/datasets/pila-"$direction"-test
  model_args=()
  model_args+=(--label 'Transformer' --inputs)
  for trial_no in "${TRIALS[@]}"; do
    model_args+=("$(get_output_name "$direction" "$trial_no")")
  done
  python pila/print_table.py "${model_args[@]}"
  echo
done
