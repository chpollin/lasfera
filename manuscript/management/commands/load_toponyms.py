from datetime import datetime

import numpy as np
import pandas as pd
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand, CommandParser
from django.db import transaction
from django.utils.text import slugify

from manuscript.models import Folio, Location, LocationAlias, SingleManuscript


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
            if is_bool:
                return self.process_bool_field(row, field_name)
            else:
                field_value = row.get(field_name)
                if field_value is not None and isinstance(field_value, str):
                    field_value = field_value.strip()
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
                df = pd.read_excel(xls, sheet_name, header=3)
                df = df.replace({np.nan: None})
                df.columns = (
                    df.columns.str.strip()
                    .str.lower()
                    .str.replace("[^\w\s]", "")
                    .str.replace(" ", "_")
                )
                dfs = {sheet_name: df}
            else:
                dfs = pd.read_excel(xls, sheet_name=None, header=3)
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
                    # we want from the Excel file the columns: Placename_ID, Label, Folio, HistEng_Name, and Comments.
                    # The following columns correspond to the fields in the Location model:
                    # 1. Placename_ID -> placename_id
                    # 2. Label -> country
                    # 3. Folio -> related_folio (this is a FK to the Folio model)
                    # 4. HistEng_Name -> belongs to the LocationAlias model and the field placename_from_mss
                    # 5. Comments -> description
                    placename_id = self.process_field(row, "placename_id", index)
                    country = self.process_field(row, "label", index)
                    folio = self.process_field(row, "folio", index)
                    placename_from_mss = self.process_field(row, "histeng_name", index)
                    description = self.process_field(row, "comments", index)
                    siglum = self.process_field(row, "ms", index)

                    try:
                        manuscript = SingleManuscript.objects.get(siglum=siglum)
                    except ObjectDoesNotExist:
                        self.stdout.write(
                            self.style.ERROR(
                                f"Manuscript with siglum '{siglum}' does not exist."
                            )
                        )
                        continue

                    try:
                        folio_obj = Folio.objects.get(
                            folio_number=folio, manuscript=manuscript
                        )
                        self.stdout.write(f"Folio object: {folio_obj}")
                    except ObjectDoesNotExist:
                        self.stdout.write(
                            self.style.ERROR(
                                f"Folio with folio number '{folio}' does not exist'"
                            )
                        )
                        continue

                    if folio_obj is not None:
                        try:
                            print(f"placename_id: {placename_id}")
                            print(f"country: {country}")
                            print(f"folio_obj: {folio_obj}")
                            print(f"description: {description}")

                            with transaction.atomic():
                                location = Location.objects.get_or_create(
                                    placename_id=placename_id,
                                    country=country,
                                    related_folio=folio_obj,
                                    description=description,
                                )

                            if placename_from_mss is not None:
                                with transaction.atomic():
                                    LocationAlias.objects.update_or_create(
                                        location=location,
                                        placename_from_mss=placename_from_mss,
                                    )
                        except Exception as e:
                            raise e

        except Exception as e:
            raise e
