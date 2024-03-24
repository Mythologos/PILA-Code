set -e
set -u

. "$(dirname "$BASH_SOURCE")"/include.bash

bash experiments/submit-job.bash \
  split+pila \
  "$LOG_DIR"/outputs \
  cpu \
  bash pila/split_data.bash "$PILA_DATA_DIR"
