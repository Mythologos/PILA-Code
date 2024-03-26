from dataclasses import dataclass, Field, fields
from typing import Iterator


@dataclass
class EtymologyPair:
    headword: str
    ancestors: list[str]

    def __iter__(self) -> Iterator:
        current_fields: list[Field] = []
        for field in fields(EtymologyPair):
            current_fields.append(self.__getattribute__(field.name))
        return (field_value for field_value in current_fields)
