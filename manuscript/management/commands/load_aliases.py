# The following script reads the "Toponym Variants" sheet from the Excel file
# and creates a new ToponymVariant object for each row. It also associates the
# toponym variant with the corresponding toponym object. The field we want to write to
# for these variants is "placename_from_mss" for each toponym object.

# The script is similar to the load_toponyms.py script, but with some modifications
# to accommodate the different fields and relationships.

import logging

import numpy as np
import pandas as pd
from django.core.management.base import BaseCommand
from django.db import IntegrityError, transaction

from manuscript.models import Location, LocationAlias

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help_text = "Load data from an Excel file. This reads information about the toponym variants and imports them."

    def add_arguments(self, parser):
        parser.add_argument(
            "--filepath", type=str, help="filepath of excel file to load"
        )
        parser.add_argument("--sheetname", type=str, help="name of sheet to load")

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

    def process_field(self, row, field_name, index, is_bool=False):
        try:
            field_value = row.get(field_name)
            if field_value is not None and isinstance(field_value, str):
                field_value = field_value.strip()
            return field_value
        except Exception as e:
            self.handle_error(index, e, row, field_name, row.get(field_name))
            raise e

    def create_location_alias(self, place_id, toponym):
        try:
            # Look up the Location instance using place_id
            locations = Location.objects.filter(placename_id=place_id)

            if not locations.exists():
                logger.error("Location with placename_id %s does not exist", place_id)
                return

            for location in locations:
                # Create or get the LocationAlias
                location_alias, created = LocationAlias.objects.get_or_create(
                    location=location,
                    placename_from_mss=toponym,
                )
                if created:
                    logger.info("Created new LocationAlias: %s", location_alias)
                else:
                    logger.info("LocationAlias already exists: %s", location_alias)
        except IntegrityError as e:
            logger.error("Integrity error creating LocationAlias: %s", e)
        except IntegrityError as e:
            logger.error("Integrity error creating LocationAlias: %s", e)
        except Exception as e:
            logger.error("Error creating LocationAlias: %s", e)

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
                    place_id = self.process_field(row, "place_id", index)
                    toponym = self.process_field(row, "toponym", index)

                    try:
                        self.create_location_alias(place_id, toponym)
                    except IntegrityError as e:
                        logger.error("Integrity error creating LocationAlias: %s", e)
                    except Exception as e:
                        logger.error("Error creating LocationAlias: %s", e)

        except Exception as e:
            logger.error("Error loading data: %s", e)
            raise e
