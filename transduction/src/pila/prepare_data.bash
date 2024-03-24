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

mkdir -p "$data_dir"/pila-{forward,backward}-{train,valid,test}
for split in train valid test; do
  ln -sf ../pila-"$split"/etyma.seg "$data_dir"/pila-forward-"$split"/source.seg
  ln -sf ../pila-"$split"/reflexes.seg "$data_dir"/pila-forward-"$split"/target.seg
  ln -sf ../pila-"$split"/reflexes.seg "$data_dir"/pila-backward-"$split"/source.seg
  ln -sf ../pila-"$split"/etyma.seg "$data_dir"/pila-backward-"$split"/target.seg
done

for direction in forward backward; do
  train_dir=$data_dir/pila-$direction-train
  for split in valid test; do
    for side in source target; do
      split_subdir=$train_dir/datasets/pila-$direction-$split
      mkdir -p "$split_subdir"
      ln -sf \
        ../../../pila-"$direction"-"$split"/"$side".seg \
        "$split_subdir"/"$side".seg
    done
  done
  bash sequence_to_sequence/prepare_data.bash \
    --training-data "$train_dir" \
    --prepare-both "$train_dir"/datasets/pila-"$direction"-valid \
    --prepare-both "$train_dir"/datasets/pila-"$direction"-test \
    --shared-vocabulary
done
