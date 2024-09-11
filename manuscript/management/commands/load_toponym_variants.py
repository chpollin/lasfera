import logging
import traceback

import numpy as np
import pandas as pd
from django.core.management.base import BaseCommand
from django.db import IntegrityError, transaction

from manuscript.models import Folio, Location, LocationAlias, SingleManuscript

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
        logger.debug("Row data: \n%s", row)

    def process_bool_field(self, row, field_name, default_value=True):
        try:
            field_value = str(row.get(field_name)).lower()
            if "yes" in field_value:
                return True
            elif "no" in field_value:
                return False
            else:
                return default_value
        except ValueError as e:
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
            "--filepath",
            type=str,
            help="filepath of excel file to load",
            default="data/tt_place_lasfera.xlsx",
        )
        parser.add_argument(
            "--sheetname", type=str, help="name of sheet to load", default="Place_IDs"
        )

    def handle(self, *args, **options):
        filepath = options.get("filepath")
        sheet_name = options.get("sheetname")

        try:
            with transaction.atomic():
                self.load_data(filepath, sheet_name)
                logger.info("Data loaded successfully")
        except FileNotFoundError as e:
            logger.error("Error loading data: %s.", e)

    def load_data(self, filepath: str, sheet_name: str):
        try:
            logger.info("Loading data from %s sheet %s", filepath, sheet_name)
            xls = pd.ExcelFile(filepath)

            if sheet_name:
                df = pd.read_excel(xls, sheet_name)
                df = df.replace({np.nan: None})
                df.columns = (
                    df.columns.str.strip()
                    .str.lower()
                    .str.replace("[^\w\s]", "")
                    .str.replace(" ", "_")
                )
                dfs = {sheet_name: df}
            else:
                dfs = pd.read_excel(xls, sheet_name=None)
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
                    placename_id = self.process_field(row, "place_id", index)
                    if not placename_id:
                        logger.warning(
                            "Skipping row %d due to empty placename_id", index
                        )
                        continue

                    variants = self.process_field(row, "label", index)
                    if variants:
                        variants = variants.split(",")
                    else:
                        logger.warning("Skipping row %d due to empty variants", index)
                        continue

                    try:
                        # find the records by placename_id
                        locations = Location.objects.filter(placename_id=placename_id)
                        if not locations.exists():
                            logger.error(
                                "Location with placename_id %s does not exist",
                                placename_id,
                            )
                            continue

                        for location in locations:
                            # then, update the LocationAlias variants
                            for variant in variants:
                                location.locationalias_set.update_or_create(
                                    placename_alias=variant.strip()
                                )

                    except IntegrityError:
                        logger.error(
                            "Error creating location: %s", traceback.format_exc()
                        )

        except Exception as e:
            raise e
