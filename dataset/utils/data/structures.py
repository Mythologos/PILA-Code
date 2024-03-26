from typing import NamedTuple, Union


PhoneSequence = list[str]
MonolingualCognateList = list[PhoneSequence]
CognateSet = tuple[MonolingualCognateList, MonolingualCognateList]
CognateSets = list[CognateSet]

FormSets = list[set[str]]
MatchList = list[tuple[int, int]]


class PILARawEntry(NamedTuple):
    base_reflex: str
    base_etyma: list[str]
    lemma: str
    base_tags: list[str]
    inflected_reflex: str
    inflected_etyma: list[str]
    inflected_tags: list[str]
    pos: str
    inflection_class: Union[int, str]
    irregularities: list[str]
    source: str
    gloss: str
    gloss_source: str
