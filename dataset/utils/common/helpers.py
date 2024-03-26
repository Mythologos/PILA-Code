from typing import Union


def display_templatic_results(results: dict[str, float], header: str):
    results_message: str = header
    for key, value in results.items():
        header: str = key.replace("_", " ").title()
        if isinstance(value, float):
            display_value: Union[int, float] = round(value, 4)
        else:
            display_value = value
        results_message += f"\n\t* {header}: {display_value}"
    else:
        results_message += "\n"
    print(results_message)
