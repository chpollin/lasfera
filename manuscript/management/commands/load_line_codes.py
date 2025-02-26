import logging
import re

import pandas as pd
from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand

from manuscript.models import LineCode, Location

logger = logging.getLogger(__name__)


def validate_line_number_code(value):
    pattern = r"^\d{2}\.\d{2}\.\d{2}(-\d{2}\.\d{2}\.\d{2})?$"
    if not re.match(pattern, value):
        raise ValidationError(
            'Invalid number format. Expected format: "01.01.04" or "01.01.04-01.01.16"'
        )


class Command(BaseCommand):
    help_text = "Load data from an Excel file. This reads information about the toponym variants and imports them."

    def add_arguments(self, parser):
        parser.add_argument(
            "--filepath",
            type=str,
            help="filepath of excel file to load",
            default="tt_place_lasfera.xlsx",
        )
        parser.add_argument(
            "--sheetname",
            type=str,
            help="name of sheet to load",
            default="PID-Line Codes",
        )
        parser.add_argument(
            "--clear-existing",
            action="store_true",
            help="Clear existing toponyms for line codes before adding new ones",
        )

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

    def handle(self, *args, **options):
        filepath = options["filepath"]
        sheetname = options.get("sheetname")
        clear_existing = options.get("clear_existing", False)

        try:
            df = pd.read_excel(filepath, sheet_name=sheetname)
            logger.debug("DataFrame columns: %s", df.columns)
        except Exception as e:
            logger.error("Error reading Excel file: %s", e)
            return

        # Print the DataFrame columns to verify the actual column names
        print("DataFrame columns:", df.columns)

        for index, row in df.iterrows():
            try:
                logger.debug("Processing row %s: %s", index + 1, row)
                line_code = self.process_field(row, "line_code", index)
                toponym_id = self.process_field(row, "id", index)

                logger.debug("line_code: %s, toponym_id: %s", line_code, toponym_id)

                if not line_code or not toponym_id:
                    logger.warning("Missing line_code or id at row %s", index + 1)
                    continue

                # Validate line_code
                validate_line_number_code(line_code)

                # Get the associated toponym
                try:
                    toponym = Location.objects.get(placename_id=toponym_id)
                except Location.DoesNotExist:
                    logger.warning(
                        "Toponym with id %s does not exist at row %s",
                        toponym_id,
                        index + 1,
                    )
                    continue

                # Get or create the LineCode instance
                line_code_obj, created = LineCode.objects.get_or_create(code=line_code)

                # If clear_existing flag is set and this is an existing line code,
                # clear all existing toponyms first
                if clear_existing and not created:
                    line_code_obj.associated_toponyms.clear()

                # Add the toponym to the line code's associated toponyms
                line_code_obj.associated_toponyms.add(toponym)

                logger.info("Successfully processed row %s", index + 1)

            except Exception as e:
                self.handle_error(index, e, row, "line_code", row.get("Line Code"))
