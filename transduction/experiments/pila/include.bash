ROOT_DIR=$(cd "$(dirname "$BASH_SOURCE")"/../.. && pwd)
. "$ROOT_DIR"/experiments/include.bash
LOG_DIR=$HOME/Private/logs/2024-03-20/pila
PILA_DATA_DIR=$DATA_DIR/pila-2024-03-20
TRIALS=({1..10})
TRIALS=(1)

get_output_name() {
  local direction=$1
  local trial_no=$2
  local result=$LOG_DIR/$direction/$trial_no
  echo -n "$result"
}
