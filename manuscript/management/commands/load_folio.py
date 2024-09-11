from datetime import datetime

import numpy as np
import pandas as pd
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand, CommandParser
from django.db import transaction
from django.utils.text import slugify

from manuscript.models import Folio, SingleManuscript


class Command(BaseCommand):
    help_text = "Load data from an Excel file. This reads information about the libraries and imports them."

    def handle_error(self, index, e, row, column_name, column_value):
        self.stdout.write(
            self.style.ERROR(
                f"Error loading data at row {index + 1}, column '{column_name}' with value '{column_value}': {type(e)} - {e}"
            )
        )
        self.stdout.write(self.style.ERROR(f"Row data: \n{row}"))

    def process_bool_field(self, row, field_name, default_value=True):
        try:
            field_value = str(row.get(field_name)).lower()
            if "yes" in field_value:
                return True
            elif "no" in field_value:
                return False
            else:
                return default_value
        except Exception as e:
            print(f"An error occurred in processing a bool field: {e}")
            return default_value

    def process_field(self, row, field_name, index, is_bool=False):
        try:
            field_value = row.get(field_name)
            if field_value is None:
                print(f"Row {index}: {field_name} is None")
            elif isinstance(field_value, str):
                field_value = field_value.strip()
                if not field_value:
                    print(
                        f"Row {index}: {field_name} is an empty string after stripping"
                    )
            return field_value
        except Exception as e:
            self.handle_error(index, e, row, field_name, row.get(field_name))
            raise e

    def add_arguments(self, parser):
        parser.add_argument(
            "--filepath", type=str, help="filepath of excel file to load"
        )
        parser.add_argument("--sheetname", type=str, help="name of sheet to load")

    def handle(self, *args, **options):
        filepath = options.get("filepath")
        sheet_name = options.get("sheetname")

        try:
            with transaction.atomic():
                self.load_data(filepath, sheet_name)
                self.stdout.write(self.style.SUCCESS("Data loaded successfully"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error loading data: {e}."))

    def load_data(self, filepath: str, sheet_name: str):
        try:
            self.stdout.write(
                self.style.SUCCESS(f"Loading data from {filepath} sheet {sheet_name}")
            )
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
                print(f"Sheet: {sheet_name} after processing columns")
                print(df.head())
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
                    print(f"Sheet: {sheet_name} after processing columns")
                    print(df.head())
                    dfs[sheet_name] = df

            for sheet_name, df in dfs.items():
                for index, row in df.iterrows():
                    folio = self.process_field(row, "folio", index)
                    manuscript_siglum = self.process_field(row, "ms", index)

                    self.stdout.write(
                        self.style.SUCCESS(
                            f"Creating folio '{folio}' for manuscript '{manuscript_siglum}'"
                        )
                    )

                    manuscripts = SingleManuscript.objects.filter(
                        siglum=manuscript_siglum
                    )
                    if not manuscripts.exists():
                        self.stdout.write(
                            self.style.ERROR(
                                f"A manuscript with siglum '{manuscript_siglum}' does not exist."
                            )
                        )
                        continue

                    for manuscript in manuscripts:
                        Folio.objects.get_or_create(
                            folio_number=folio,
                            manuscript=manuscript,
                        )

        except Exception as e:
            raise e
