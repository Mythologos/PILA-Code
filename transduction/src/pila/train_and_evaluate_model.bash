set -e
set -u
set -o pipefail

usage() {
  echo "Usage: $0 <output-dir> <data-dir> <direction> ..."
}

output_dir=${1-}
data_dir=${2-}
direction=${3-}
if ! shift 3; then
  usage >&2
  exit 1
fi
extra_args=("$@")

train_name=pila-$direction-train
test_name=pila-$direction-test

train_dir=$data_dir/$train_name
valid_dir=$train_dir/datasets/pila-$direction-valid
vocab_type=shared

model_size=$(python utils/random_sample.py --int 4 64)
dropout=$(python utils/random_sample.py 0 0.2)
learning_rate=$(python utils/random_sample.py --log 0.0001 0.01)
batching_max_tokens=$(python utils/random_sample.py --int 32 256)

num_heads=8
dmodel=$(( num_heads * model_size ))
layers=6
model_args=( \
  --d-model "$dmodel" \
  --num-heads "$num_heads" \
  --feedforward-size "$(( 4 * dmodel ))" \
  --dropout "$dropout" \
  --init-scale 0.01 \
  --encoder-layers "$layers" \
  --decoder-layers "$layers" \
)

python sequence_to_sequence/train.py \
  --training-data-source "$train_dir"/source."$vocab_type".prepared \
  --training-data-target "$train_dir"/target."$vocab_type".prepared \
  --validation-data-source "$valid_dir"/source."$vocab_type".prepared \
  --validation-data-target "$valid_dir"/target."$vocab_type".prepared \
  --shared-vocabulary "$train_dir"/both.vocab \
  --output "$output_dir" \
  "${model_args[@]}" \
  --epochs 100 \
  --optimizer Adam \
  --learning-rate "$learning_rate" \
  --label-smoothing 0.1 \
  --gradient-clipping-threshold 5 \
  --early-stopping-patience 4 \
  --learning-rate-patience 2 \
  --learning-rate-decay-factor 0.5 \
  --checkpoint-interval-sequences 2000 \
  --batching-max-tokens "$batching_max_tokens" \
  "${extra_args[@]}"
bash pila/evaluate_model.bash \
  "$data_dir" \
  "$train_name" \
  "$test_name" \
  "$output_dir"
