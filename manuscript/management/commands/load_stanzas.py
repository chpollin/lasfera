import logging

import numpy as np
import pandas as pd
from django.core.management.base import BaseCommand
from django.db import transaction

from manuscript.models import SingleManuscript, Stanza

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help_text = "Load data from an Excel file. This reads information about the libraries and imports them."

    def handle_error(self, index, e, row, column_name, column_value):
        logger.error(
            "Error loading data at row %s, column '%s' with value '%s': %s - %s",
            index + 1,
            column_name,
            column_value,
            type(e),
            e,
        )
        logger.error("Row data: \n%s", row)

    def process_field(self, row, field_name, index):
        try:
            field_value = row.get(field_name)
            if field_value is not None and isinstance(field_value, str):
                field_value = field_value.strip()
            return field_value
        except Exception as e:
            self.handle_error(index, e, row, field_name, row.get(field_name))
            raise e

    def add_arguments(self, parser):
        parser.add_argument(
            "--filepath",
            type=str,
            help="filepath of excel file to load",
        )
        parser.add_argument("--sheetname", type=str, help="name of sheet to load")

    def handle(self, *args, **options):
        filepath = options.get("filepath")
        sheet_name = options.get("sheetname")

        try:
            with transaction.atomic():
                self.load_data(filepath, sheet_name)
                self.stdout.write(self.style.SUCCESS("Data loaded successfully"))
        except FileNotFoundError as e:
            self.stdout.write(self.style.ERROR(f"Error loading data: {e}."))

    def load_data(self, filepath: str, sheet_name: str):
        try:
            logger.info("Loading data from %s sheet %s", filepath, sheet_name)
            xls = pd.ExcelFile(filepath)

            if sheet_name:
                df = pd.read_excel(xls, sheet_name, header=0)
                df = df.replace({np.nan: None})
                df.columns = (
                    df.columns.str.strip()
                    .str.lower()
                    .str.replace("[^\w\s]", "")
                    .str.replace(" ", "_")
                )
                dfs = {sheet_name: df}
            else:
                dfs = pd.read_excel(xls, sheet_name=None, header=0)
                for sheet_name, df in dfs.items():
                    df = df.replace({np.nan: None})
                    df.columns = (
                        df.columns.str.strip()
                        .str.lower()
                        .str.replace("[^\w\s]", "")
                        .str.replace(" ", "_")
                    )
                    dfs[sheet_name] = df

            for sheet_name, df in dfs.items():
                for index, row in df.iterrows():
                    manuscript = SingleManuscript.objects.get(siglum="Urb1")
                    line_code = self.process_field(row, "code", index)
                    if line_code is None:
                        logger.error("Missing line code at index %s", index)
                        continue
                    text = self.process_field(row, "italian", index)

                    # We create a new stanza object with their stanza_line_code_starts and stanza_text
                    # We need to convert the line code from, e.g., 1.1.2 to 01.01.02.
                    line_code = line_code.split(".")
                    line_code = [f"{int(x):02d}" for x in line_code]
                    line_code = ".".join(line_code)
                    stanza, created = Stanza.objects.get_or_create(
                        related_manuscript=manuscript,
                        stanza_line_code_starts=line_code,
                        stanza_text=text,
                    )

                    if created:
                        logger.info("Created stanza %s", stanza.stanza_line_code_starts)

        except Exception as e:
            logger.exception("An error occurred:", exc_info=e)
            raise e
