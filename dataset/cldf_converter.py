from argparse import ArgumentParser, FileType, Namespace
from typing import TextIO

from csvw import Column
from pycldf import Wordlist

from utils.common import ConverterMessage
from utils.data import build_tables, DefinedSource, GLOSS_TABLE_COLUMNS, LEMMA_TABLE_COLUMNS, PILARawEntry, \
    TAG_TABLE_COLUMNS


def extract_etyma(current_etyma: str) -> list[str]:
    etyma_strings: list[str] = current_etyma.strip("[]").split(" ")
    for i in range(0, len(etyma_strings)):
        etyma_strings[i] = etyma_strings[i].strip("'")
    return etyma_strings


def process_base_file(input_file: TextIO) -> list[PILARawEntry]:
    entries: list[PILARawEntry] = []
    for line_index, line in enumerate(input_file):
        base_reflex, base_etyma, lemma, pos, inflection_class, base_morph_tags, inflected_reflex, inflected_etyma, \
            inflected_morph_tags, _, row_irregularities, cut_bool, addition_bool, gloss, gloss_source = line.split("\t")

        if cut_bool.strip() == "TRUE" or line_index == 0:
            continue
        else:
            source: str = DefinedSource.DE_VAAN if addition_bool.strip() == "TRUE" else DefinedSource.WIKTIONARY

        etyma: list[str] = extract_etyma(base_etyma)
        morph_tags: list[str] = base_morph_tags.strip().split("-")
        irregularities: list[str] = [
            irregularity.strip().title() for irregularity in row_irregularities.strip().split(", ")
            if irregularity.strip() != ""
        ]

        if all([item != "" for item in (inflected_reflex, inflected_etyma, inflected_morph_tags)]) is True:
            form_etyma: list[str] = extract_etyma(inflected_etyma)
            form_morph_tags: list[str] = inflected_morph_tags.strip().split("-")
        else:
            form_etyma: list[str] = []
            form_morph_tags: list[str] = []

        base_reflex: str = base_reflex.strip()
        inflected_reflex: str = inflected_reflex.strip()
        new_entry: PILARawEntry = PILARawEntry(
            base_reflex, etyma, lemma.lower(), morph_tags, inflected_reflex, form_etyma, form_morph_tags,
            pos.strip(), inflection_class.strip(), irregularities, source, gloss.strip(), gloss_source.strip()
        )
        entries.append(new_entry)

    return entries


if __name__ == "__main__":
    parser: ArgumentParser = ArgumentParser()
    parser.add_argument("input_file", type=FileType(encoding="utf-8", mode="r"), help=ConverterMessage.INPUT_FILE)
    parser.add_argument("--output-directory", type=str, default="cldf", help=ConverterMessage.OUTPUT_DIRECTORY)
    args: Namespace = parser.parse_args()

    dataset: Wordlist = Wordlist.in_dir(args.output_directory)
    print("Collecting entries...")
    base_entries: list[PILARawEntry] = process_base_file(args.input_file)
    print("Building tables...")
    dataset_tables, sources = build_tables(base_entries)

    dataset.add_sources(*sources)
    print("Writing dataset...")
    for table_name in dataset_tables.keys():
        if table_name not in ("FormTable", "glosses.csv", "lemmata.csv", "tags.csv"):
            dataset.add_component(table_name)
        elif table_name == "FormTable":
            dataset.add_columns("FormTable", "Gloss_ID")
            dataset.add_columns("FormTable", "Lemma_ID")
            dataset.add_columns("FormTable", "Tag_ID")

            # It doesn't seem like there's an easy way to reorder columns via the library. So, I do it manually here.
            table = dataset.get("FormTable")
            columns = table.tableSchema.columns
            id_column, lang_id_column, parameter_id_column, form_column, segments_column, comment_column, \
                source_column, gloss_id_column, lemma_id_column, tag_id_column = columns
            revised_columns: list[Column] = [
                id_column, lang_id_column, parameter_id_column, lemma_id_column, gloss_id_column, tag_id_column,
                form_column, segments_column, comment_column, source_column
            ]
            table.tableSchema.columns = revised_columns
        elif table_name == "glosses.csv":
            dataset.add_table("glosses.csv", *GLOSS_TABLE_COLUMNS, primaryKey="ID")
            dataset.add_foreign_key("FormTable", "Gloss_ID", "glosses.csv", "ID")
        elif table_name == "lemmata.csv":
            dataset.add_table("lemmata.csv", *LEMMA_TABLE_COLUMNS, primaryKey="ID")
            dataset.add_foreign_key("FormTable", "Lemma_ID", "lemmata.csv", "ID")
        elif table_name == "tags.csv":
            dataset.add_table("tags.csv", *TAG_TABLE_COLUMNS, primaryKey="ID")
            dataset.add_foreign_key("FormTable", "Tag_ID", "tags.csv", "ID")
        else:
            continue

    dataset.write(**dataset_tables)
    print("Validating dataset...")
    dataset.validate()
