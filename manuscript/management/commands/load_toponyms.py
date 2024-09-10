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

    def create_location(
        self,
        placename_id,
        description,
        place_type,
        latitude,
        longitude,
        georef,
        country,
        folio,
        manuscript,
    ):
        try:
            location, created = Location.objects.get_or_create(
                placename_id=placename_id,
                description=description,
                place_type=place_type,
                latitude=latitude,
                longitude=longitude,
                authority_file=georef,
                modern_country=country,
            )

            # Assign the folio ManyToManyField
            try:
                folio = Folio.objects.get(
                    folio_number=folio, manuscript__siglum=manuscript
                )
                folio.locations_mentioned.add(location)
                folio.save()
            except Exception as e:
                logger.error("Error associating folio to location: %s", e)

            logger.info("Location %s created: %s", location, created)
        except IntegrityError:
            location = Location.objects.get(placename_id=placename_id)
            logger.info("Location already exists: %s", location)
        return location

    def create_location_alias(self, placename_id, place_name_from_mss):
        LocationAlias.objects.update_or_create(
            placename_id=placename_id, placename_from_mss=place_name_from_mss
        )

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
                    description = self.process_field(row, "comments", index)
                    place_type = self.process_field(row, "place_type", index)
                    latitude = self.process_field(row, "latitude", index)
                    longitude = self.process_field(row, "longitude", index)
                    georef = self.process_field(row, "geo_ref", index)
                    modern_country = self.process_field(row, "mod_name", index)
                    folio = self.process_field(row, "folio", index)
                    manuscript = self.process_field(row, "ms", index)

                    try:
                        self.create_location(
                            placename_id,
                            description,
                            place_type,
                            latitude,
                            longitude,
                            georef,
                            modern_country,
                            folio,
                            manuscript,
                        )
                    except IntegrityError:
                        logger.error(
                            "Error creating location: %s", traceback.format_exc()
                        )

        except Exception as e:
            raise e
