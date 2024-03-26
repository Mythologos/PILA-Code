
def display_dataset_results(results: dict[str, dict[str, int]], dataset_name: str):
    results_string: str = f"Results for <{dataset_name}>:"
    for proto_language, matches in results.items():
        results_string += f"\n\t* {proto_language}"
        for match_language, count in matches.items():
            results_string += f"\n\t\t- {match_language}: {count}"
        results_string += "\n"
    print(results_string)


def display_maximum_results(results_per_dataset: dict[str, dict[str, dict[str, int]]]):
    for current_dataset, current_dataset_results in results_per_dataset.items():
        all_pairs: list[tuple[str, str, int]] = []
        for proto_language, reflex_languages in current_dataset_results.items():
            if proto_language == "unmatched":
                continue
            else:
                for reflex_language, frequency in reflex_languages.items():
                    pair_with_frequency: tuple[str, str, int] = (proto_language, reflex_language, frequency)
                    all_pairs.append(pair_with_frequency)
        maximum_pair = max(all_pairs, key=lambda x: x[-1])
        maximum_proto, maximum_reflex, maximum_frequency = maximum_pair
        print(f"The maximum pair for <{current_dataset}> is <{maximum_proto}> and <{maximum_reflex}> "
              f"at <{maximum_frequency}>.")
