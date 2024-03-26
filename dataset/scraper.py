from argparse import ArgumentParser, Namespace
from os.path import isfile
from typing import Any, TextIO

from natsort import natsorted
from scrapy.crawler import CrawlerProcess

from utils.common import ScraperMessage
from utils.scraping import DEFAULT_FILTERS, DEFAULT_INPUT_FILEPATH, DEFAULT_OUTPUT_FILEPATH, DEFAULT_SPIDER_SETTINGS, \
    FilterType, WiktionarySpider


def get_urls(input_filepath: str) -> list[str]:
    wiktionary_urls: list[str] = []
    with open(input_filepath, encoding="utf-8", mode="r") as input_file:
        for line in input_file:
            if not line.startswith("#"):
                wiktionary_urls.append(line.strip())
        else:
            if not wiktionary_urls:
                raise ValueError(f"The given filepath, <{args.input_filepath}>, contains no URLs. "
                                 f"Please supply a file with URLs.")

    return wiktionary_urls


if __name__ == "__main__":
    parser: ArgumentParser = ArgumentParser()
    parser.add_argument(
        "--filters", type=str, nargs='+', choices=list(FilterType), default=DEFAULT_FILTERS, help=ScraperMessage.FILTERS
    )
    parser.add_argument(
        "--input-filepath", type=str, default=DEFAULT_INPUT_FILEPATH, help=ScraperMessage.INPUT_FILEPATH
    )
    parser.add_argument(
        "--output-filepath", type=str, default=DEFAULT_OUTPUT_FILEPATH, help=ScraperMessage.OUTPUT_FILEPATH
    )
    args: Namespace = parser.parse_args()

    # Verify inputs.
    if not isfile(args.input_filepath):
        raise ValueError(f"The given filepath, <{args.input_filepath}>, is not a valid filepath. "
                         f"Please try again.")

    # Read in URL(s) from file; for now, the code assumes that all lines in files will be valid URLs,
    # save those that begin with Python's comment character ("#").
    urls: list[str] = get_urls(args.input_filepath)

    # Submit URLs to Spider for scraping, along with any desired options.
    # Also, set desired options for scraping in order to supply it to the scraper.
    settings: dict[str, Any] = DEFAULT_SPIDER_SETTINGS

    scrape_results: dict[str, list[str]] = {}
    recorded_failures: list[str] = []

    process: CrawlerProcess = CrawlerProcess(settings=settings)
    process.crawl(WiktionarySpider, urls, scrape_results, recorded_failures)
    process.start()

    sorted_results: list = natsorted(scrape_results.items(), key=lambda key_value_pair: key_value_pair[0])

    main_files: dict[str, TextIO] = {"main": open(args.output_filepath, mode="w+", encoding="utf-8")}
    start, extension = args.output_filepath.rsplit(".", 1)
    for filter_name in args.filters:
        filter_filepath: str = f"{start}_{filter_name}.{extension}"
        main_files[filter_name] = open(filter_filepath, mode="w+", encoding="utf-8")

    for (key, value) in sorted_results:
        output: str = f"{key}, {value}\n"
        if "-" in key:
            main_files[FilterType.AFFIX].write(output)
        elif "*" in key:
            main_files[FilterType.RECONSTRUCTION].write(output)
        else:
            main_files["main"].write(output)

    for file in main_files.values():
        file.close()

    output_error_filepath: str = f"{start}_errors.{extension}"
    with open(output_error_filepath, mode="w+", encoding="utf-8") as error_file:
        for failure in recorded_failures:
            error_file.write(f"{failure}\n")
