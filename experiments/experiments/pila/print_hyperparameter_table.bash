set -e
set -u
set -o pipefail

. "$(dirname "$BASH_SOURCE")"/include.bash

cd "$ROOT_DIR"/src

get_left_or_right() {
  local direction=$1
  case $direction in
    forward) result=right ;;
    backward) result=left ;;
    *) return 1;;
  esac
  printf %s "$result"
}

model_args=()
for direction in forward backward; do
  model_args+=(--label "Proto-Italic \$\\$(get_left_or_right "$direction")arrow\$ Latin" --inputs)
  for trial_no in "${TRIALS[@]}"; do
    model_args+=("$(get_output_name "$direction" "$trial_no")")
  done
done
python pila/print_hyperparameter_table.py "${model_args[@]}"
