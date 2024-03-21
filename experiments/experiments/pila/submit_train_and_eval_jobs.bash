set -e
set -u

. "$(dirname "$BASH_SOURCE")"/include.bash

for trial_no in "${TRIALS[@]}"; do
  for direction in forward backward; do
    bash experiments/submit-job.bash \
      pila+"$direction"+"$trial_no" \
      "$LOG_DIR"/outputs \
      gpu \
      bash pila/train_and_evaluate_model.bash \
        "$LOG_DIR"/"$direction"/"$trial_no" \
        "$PILA_DATA_DIR" \
        "$direction" \
        --no-progress
  done
done
