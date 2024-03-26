from argparse import ArgumentParser, Namespace, BooleanOptionalAction

from utils.common import ProtoMessage
from utils.studies.proto import PROTO_DATASET_FILEPATHS, PROTO_DATASET_LOADERS, \
    DefinedProtoDataset, ProtoMapping, ProtoLoader, display_dataset_results, display_maximum_results


if __name__ == "__main__":
    parser: ArgumentParser = ArgumentParser()
    parser.add_argument(
        "--datasets", type=str, nargs="+", default=list(DefinedProtoDataset),
        choices=list(DefinedProtoDataset), help=ProtoMessage.DATASETS
    )
    parser.add_argument(
        "--display-maxima", action=BooleanOptionalAction, default=False, help=ProtoMessage.DISPLAY_MAXIMA
    )
    args: Namespace = parser.parse_args()

    results_by_dataset: dict[str, dict[str, dict[str, int]]] = {}
    for dataset in args.datasets:
        print(f"Computing results on <{dataset}>...")
        dataset_path: str = PROTO_DATASET_FILEPATHS[dataset]
        dataset_loader: ProtoLoader = PROTO_DATASET_LOADERS[dataset]
        dataset_results: ProtoMapping = dataset_loader(dataset_path, dataset)
        results_by_dataset[dataset] = dataset_results
        if args.display_maxima is False:
            display_dataset_results(dataset_results, dataset)

    if args.display_maxima is True:
        print("Displaying maximum results...")
        display_maximum_results(results_by_dataset)
