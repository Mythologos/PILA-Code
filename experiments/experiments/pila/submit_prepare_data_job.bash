set -e
set -u

. "$(dirname "$BASH_SOURCE")"/include.bash

bash experiments/submit-job.bash \
  prepare+pila \
  "$LOG_DIR"/outputs \
  cpu \
  bash pila/prepare_data.bash "$PILA_DATA_DIR"
