from typing import Sequence

from .constants import BASE_URL, COMBINED_DIACRITIC_VOWELS, COMMON_SERIES_TERMS, COMMON_SPLIT_VALUES, \
    DEFAULT_INPUT_FILEPATH, DEFAULT_OUTPUT_FILEPATH, DEFAULT_SPIDER_SETTINGS, ETYMOLOGY_HEADER_QUERY, \
    ETYMOLOGY_PARENTHESES_PATTERN, ETYMOLOGY_SLASH_PATTERN, LATIN_SECTION_QUERY_A, LATIN_SECTION_QUERY_B, \
    LATIN_WORD_QUERY, LIST_XPATH_QUERY, NEXT_PAGE_XPATH_QUERY, PROTO_ITALIC_WORD_QUERY
from .enumerations import FilterType
from .spider import WiktionarySpider

DEFAULT_FILTERS: Sequence[str] = (FilterType.AFFIX, FilterType.RECONSTRUCTION)
