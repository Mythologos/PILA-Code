set -e
set -u

. "$(dirname "$BASH_SOURCE")"/include.bash

for trial_no in "${TRIALS[@]}"; do
  for direction in forward backward; do
    bash experiments/submit-job.bash \
      pila+"$direction"+"$trial_no" \
      "$LOG_DIR"/outputs \
      cpu \
      bash pila/rescore_model.bash \
        "$PILA_DATA_DIR" \
        pila-"$direction"-{train,test} \
        "$LOG_DIR"/"$direction"/"$trial_no"
  done
done
