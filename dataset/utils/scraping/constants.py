from typing import Any

# General Constants:
COMBINED_DIACRITIC_VOWELS: dict[str, tuple[str, str]] = {
    'Ā̆': ('Ā', 'Ă'),
    'ā̆': ('ā', 'ă'),
    'Ē̆': ('Ē', 'Ĕ'),
    'ē̆': ('ē', 'ĕ'),
    'Ī̆': ('Ī', 'Ĭ'),
    'ī̆': ('ī', 'ĭ'),
    'Ō̆': ('Ō', 'Ŏ'),
    'ō̆': ('ō', 'ŏ'),
    'Ū̆': ('Ū', 'Ŭ'),
    'ū̆': ('ū', 'ŭ')
}

COMMON_SPLIT_VALUES: tuple = (",", "~")
COMMON_SERIES_TERMS: tuple = ("or",)

# URLs:
BASE_URL: str = "https://en.wiktionary.org"

# XPaths:
LIST_XPATH_QUERY: str = "//div[@id='mw-pages']/div[@class='mw-content-ltr']/descendant::a"
NEXT_PAGE_XPATH_QUERY: str = "//div[@id='mw-pages']/child::a[contains(text(), 'next page')]/@href"
PROTO_ITALIC_WORD_QUERY: str = ".//i[@class='Latn mention' and @lang='itc-pro']/descendant-or-self::text()"
LATIN_WORD_QUERY: str = ".//strong[@class='Latn headword' and @lang='la']/descendant-or-self::text()"
ETYMOLOGY_HEADER_QUERY: str = ".//span[@class='mw-headline']/text()"

# The following use the Kayessian XPath 1.0 formula.
# See: https://stackoverflow.com/questions/3428104/selecting-siblings-between-two-nodes-using-xpath

# Query A: the section on Latin is not the last section on the list,
# so it is between the Latin header and the next <h2> header.
LATIN_SECTION_QUERY_A: str = "//h2[span[@id='Latin']]/" \
                             "following-sibling::*" \
                             "[(self::p or self::ul or self::h3) and " \
                             "count(.|//h2[span[@id='Latin']]/following-sibling::h2[1]/preceding-sibling::*) = " \
                             "count(//h2[span[@id='Latin']]/following-sibling::h2[1]/preceding-sibling::*)]"

# Query B: the section on Latin is the last section on the list.
LATIN_SECTION_QUERY_B: str = "//h2[span[@id='Latin']]/" \
                             "following-sibling::*" \
                             "[(self::p or self::ul or self::h3) and " \
                             "count(.|//div[@class='mw-content-ltr mw-parser-output']/child::*) = " \
                             "count(//div[@class='mw-content-ltr mw-parser-output']/child::*)]"

"//h2[span[@id='Latin']]/following-sibling::*[(self::p or self::ul or self::h3) and count(.|//div[@class='mw-parser-output']/child::*) = count(//div[@class='mw-parser-output']/child::*)]"

# Regular Expressions:
ETYMOLOGY_PARENTHESES_PATTERN: str = r"(?P<parenthetical>\((?P<inner_variant>.+)\))"
ETYMOLOGY_SLASH_PATTERN: str = r"(?P<slash_division>(?P<left_variant>.{1})/(?P<right_variant>.{1}))"

# CLI Values:
DEFAULT_INPUT_FILEPATH: str = "dataset/data/raw/scraping/urls/proto_italic_urls.txt"
DEFAULT_OUTPUT_FILEPATH: str = "dataset/data/raw/scraping/outputs/current/pila_main.txt"

# Spider Settings:
DEFAULT_SPIDER_SETTINGS: dict[str, Any] = {
    "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0",
    "CONCURRENT_REQUESTS": 8,
    "DOWNLOAD_DELAY": .5,
    "DOWNLOAD_TIMEOUT": 600,
    "AUTOTHROTTLE_ENABLED": True,
    "AUTOTHROTTLE_TARGET_CONCURRENCY": 0.75
}
