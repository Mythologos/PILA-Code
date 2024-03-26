from copy import deepcopy
from re import search, Match
from typing import Callable, Optional, Sequence

from scrapy import Request, Selector, Spider
from scrapy.http import Response

from .constants import BASE_URL, COMBINED_DIACRITIC_VOWELS, COMMON_SERIES_TERMS, COMMON_SPLIT_VALUES, \
    ETYMOLOGY_HEADER_QUERY, ETYMOLOGY_PARENTHESES_PATTERN, ETYMOLOGY_SLASH_PATTERN, LATIN_SECTION_QUERY_A, \
    LATIN_SECTION_QUERY_B, LATIN_WORD_QUERY, LIST_XPATH_QUERY, NEXT_PAGE_XPATH_QUERY, PROTO_ITALIC_WORD_QUERY
from .structures import EtymologyPair


class WiktionarySpider(Spider):
    SPIDER_NAME: str = "wiktionary-spider"

    def __init__(self, start_urls: list[str], results: dict[str, list[str]], failed_scrapes: list[str],
                 **kwargs):
        super(WiktionarySpider, self).__init__(name=self.SPIDER_NAME, start_urls=start_urls, kwargs=kwargs)
        self.preprocessors: dict[str, Sequence[Callable]] = {
            "latin_forms": (self.separate_diacritics, self.make_unique),
            "proto_italic_forms":
                (self.clean_series_formatting, self.split_series, self.unpack_parenthetical_variations,
                 self.unpack_slash_variations, self.separate_diacritics, self.make_unique)
        }
        self.results: dict[str, list[str]] = results
        self.failed_scrapes: list[str] = failed_scrapes

    # This method scrapes the initial page to retrieve other webpages.
    # It may also proceed to other webpages of the same type.
    def parse(self, response, **kwargs) -> Request:
        for selector in response.xpath(LIST_XPATH_QUERY):
            text: str = selector.xpath("text()").get()
            link: str = selector.attrib['href']
            yield Request(f"{BASE_URL}{link}", self.parse_proto_italic_data, cb_kwargs={"headword": text})
        else:
            next_page_link: str = response.xpath(NEXT_PAGE_XPATH_QUERY).get()
            if next_page_link:
                yield Request(f"{BASE_URL}/{next_page_link}", self.parse)

    def parse_proto_italic_data(self, response: Response, **kwargs):
        # First, we get the selectors from the Latin section. This permits us to "focus" on the relevant data.
        # It also preserves the order of elements such that we can disambiguate between which etymologies
        # go with which terms.
        selectors: list[Selector] = response.xpath(LATIN_SECTION_QUERY_A) \
            if len(response.xpath(LATIN_SECTION_QUERY_A)) > 0 \
            else response.xpath(LATIN_SECTION_QUERY_B)

        etymology_pairs: list[EtymologyPair] = []
        proto_italic_forms: list[str] = []
        latin_forms: list[str] = []
        for selector in selectors:
            # There are two valid categories of selectors:
            # <h3>s indicate headers. Some will be about etymology. These will precede the actual word listing.
            # <ul>s and <p>s give the actual content. Some will contain the Proto-Italic data;
            # others will contain the headwords.
            tag: str = selector.root.tag
            if tag == "h3":
                text: str = selector.xpath(ETYMOLOGY_HEADER_QUERY).get()
                if text and "Etymology" in text:
                    self.get_etymological_pairs(
                        latin_forms, proto_italic_forms, etymology_pairs, self.preprocessors["latin_forms"],
                        self.preprocessors["proto_italic_forms"]
                    )

                    # Finally, we clear out the lists we were using.
                    proto_italic_forms.clear()
                    latin_forms.clear()
            elif tag in ["p", "ul"]:
                selected_proto_italic_forms: list[str] = selector.xpath(PROTO_ITALIC_WORD_QUERY).getall()
                selected_latin_forms: list[str] = selector.xpath(LATIN_WORD_QUERY).getall()

                if len(selected_proto_italic_forms) > 0:
                    proto_italic_forms.extend(selected_proto_italic_forms)

                if len(selected_latin_forms) > 0:
                    if len(selected_latin_forms) > 1 and " " in selected_latin_forms:
                        selected_latin_forms = ["".join(selected_latin_forms)]
                    latin_forms.extend(selected_latin_forms)
            else:
                raise ValueError(f"Invalid tag caught by section query: '{tag}'.")
        else:
            self.get_etymological_pairs(
                latin_forms, proto_italic_forms, etymology_pairs, self.preprocessors["latin_forms"],
                self.preprocessors["proto_italic_forms"]
            )
            if len(etymology_pairs) == 0:
                self.failed_scrapes.append(kwargs["headword"])

        self.resolve_homonyms(etymology_pairs)

        for (headword, etymologies) in etymology_pairs:
            self.results[f"{headword}"] = etymologies

    @staticmethod
    def get_etymological_pairs(latin_forms: list[str], proto_italic_forms: list[str],
                               etymology_pairs: list[EtymologyPair],
                               latin_preprocessors: Optional[Sequence[Callable]] = None,
                               proto_italic_preprocessors: Optional[Sequence[Callable]] = None):
        # We have moved on to a new etymology, so the old one won't work for future terms.
        # At this point, we can pair each Latin headword with its Proto-Italic list.
        if latin_preprocessors:
            for latin_preprocessor in latin_preprocessors:
                latin_preprocessor(latin_forms)

        if proto_italic_preprocessors:
            for proto_italic_preprocessor in proto_italic_preprocessors:
                proto_italic_preprocessor(proto_italic_forms)

        for form in latin_forms:
            # We assure that there are actually forms to pair with the term.
            # If not, we're not including it in the list.
            if proto_italic_forms:
                proto_italic_forms = [pt_form.strip("*") for pt_form in proto_italic_forms]
                etymology_pair = EtymologyPair(headword=form, ancestors=deepcopy(proto_italic_forms))
                etymology_pairs.append(etymology_pair)

    @staticmethod
    def resolve_homonyms(etymology_pairs: list[EtymologyPair]):
        outer_index: int = 0
        duplicate_indices: list[int] = []
        while outer_index < len(etymology_pairs):
            first_term = etymology_pairs[outer_index].headword
            duplicate_indices.append(outer_index)
            inner_index: int = outer_index + 1
            while inner_index < len(etymology_pairs):
                second_term = etymology_pairs[inner_index].headword
                if first_term == second_term:
                    duplicate_indices.append(inner_index)
                inner_index += 1
            else:
                if len(duplicate_indices) > 1:
                    for counter, duplicate_index in enumerate(duplicate_indices, 1):
                        starting_headword: str = etymology_pairs[duplicate_index].headword
                        etymology_pairs[duplicate_index].headword = f"{starting_headword}_{counter}"

            duplicate_indices.clear()
            outer_index += 1

    @staticmethod
    def separate_diacritics(words: list[str]):
        index: int = 0
        while index < len(words):
            for diacritic_vowel in COMBINED_DIACRITIC_VOWELS.keys():
                if diacritic_vowel in words[index]:
                    combined_diacritic_word: str = words.pop(index)
                    words.insert(index, combined_diacritic_word.replace(
                        diacritic_vowel, COMBINED_DIACRITIC_VOWELS[diacritic_vowel][0]
                    ))
                    words.insert(index, combined_diacritic_word.replace(
                        diacritic_vowel, COMBINED_DIACRITIC_VOWELS[diacritic_vowel][1]
                    ))
            index += 1

    @staticmethod
    def unpack_slash_variations(words: list[str]):
        index: int = 0
        while index < len(words):
            current_word: str = words[index]
            current_match: Optional[Match] = search(ETYMOLOGY_SLASH_PATTERN, current_word)
            if current_match:
                match_groups: dict = current_match.groupdict()
                words.pop(index)
                word_splits: list[str] = current_word.split(match_groups["slash_division"])
                if len(word_splits) > 2:
                    raise NotImplementedError("This function currently does not handle multiple slash divisions.")
                else:
                    left, right = word_splits
                    words.insert(index, f"{left}{match_groups['left_variant']}{right}")
                    words.insert(index, f"{left}{match_groups['right_variant']}{right}")

            index += 1

    @staticmethod
    def unpack_parenthetical_variations(words: list[str]):
        index: int = 0
        while index < len(words):
            current_word: str = words[index]
            current_match: Optional[Match] = search(ETYMOLOGY_PARENTHESES_PATTERN, current_word)
            if current_match:
                match_groups: dict = current_match.groupdict()
                words.pop(index)
                word_splits: list[str] = current_word.split(match_groups["parenthetical"])
                if len(word_splits) > 2:
                    raise NotImplementedError("This function currently does not handle "
                                              "multiple parenthetical divisions.")
                else:
                    left, right = word_splits
                    words.insert(index, f"{left}{right}")
                    words.insert(index, f"{left}{match_groups['inner_variant']}{right}")
            index += 1

    @staticmethod
    def split_series(words: list[str], split_criteria: tuple = COMMON_SPLIT_VALUES):
        index: int = 0
        while index < len(words):
            for criterion in split_criteria:
                has_series: bool = False
                split_words: list[str] = words[index].split(criterion)
                if len(split_words) > 2:
                    has_series: bool = True
                elif len(split_words) == 2:
                    left, right = split_words
                    if left and right:
                        has_series = True

                if has_series:
                    words.pop(index)
                    for split_word in split_words:
                        stripped_word: str = split_word.strip(" " + ",")
                        if stripped_word:
                            words.insert(index, stripped_word)
            index += 1

    @staticmethod
    def clean_series_formatting(words: list[str], series_terms: tuple = COMMON_SERIES_TERMS):
        # Note: this function only works if we assume that the series terms aren't the terms themselves.
        # In our case, they are not--but that assumption may not hold in all cases.
        for term in series_terms:
            if term in words:
                index: int = 0
                while index < len(words):
                    if words[index] == term:
                        words.pop(index)
                    else:
                        words[index] = words[index].strip()
                        index += 1

    @staticmethod
    def make_unique(duplicate_list: list[str]):
        first_index: int = 0
        while first_index < len(duplicate_list):
            second_index: int = first_index + 1
            while second_index < len(duplicate_list):
                if duplicate_list[first_index] == duplicate_list[second_index]:
                    duplicate_list.pop(second_index)
                else:
                    second_index += 1
            first_index += 1
