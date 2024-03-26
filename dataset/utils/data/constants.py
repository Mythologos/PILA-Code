from string import digits


HEADWORD_NUMERATION: str = f"{digits}_"
PHONETIC_LATIN_TOKENIZER: str = "(.ː|ae(?!ː)|au(?!ː)|oe(?!ː)|qu|.+?)"
# Latin also has ei, eu, and ui, but these can't be reliably extracted from regex.
# /ae/ is rarely not a diphthong; if one of the vowels is long, the tokenizer should handle this automatically.
#   (e.g., "aeːnus" should be tokenized as "a eː n u s").

PHONETIC_PROTO_ITALIC_TOKENIZER: str = "(.ʷ|.ː|ai(?!ː)|ei(?!ː)|oi(?!ː)|au(?!ː)|eu(?!ː)|ou(?!ː)|.+?)"

DEFAULT_INPUT_FILEPATH: str = "dataset/data/raw/tsv/pila.tsv"
DEFAULT_OUTPUT_FILEPATH: str = "dataset/data/cldf"
