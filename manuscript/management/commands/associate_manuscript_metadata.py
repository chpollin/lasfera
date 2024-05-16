from datetime import datetime

import numpy as np
import pandas as pd
from django.core.management.base import BaseCommand, CommandParser
from django.db import transaction
from django.utils.text import slugify

from manuscript.models import (
    AuthorityFile,
    Codex,
    Detail,
    EditorialStatus,
    Folio,
    Library,
    Location,
    LocationAlias,
    Reference,
    SingleManuscript,
    Stanza,
    StanzaVariant,
    TextDecoration,
    ViewerNote,
)


class Command(BaseCommand):
    help_text = "Load data from an Excel file. This reads information about the libraries and imports them."

    def handle_error(self, index, e, row, column_name, column_value):
        self.stdout.write(
            self.style.ERROR(
                f"Error loading data at row {index + 1}, column '{column_name}' with value '{column_value}': {type(e)} - {e}"
            )
        )
        self.stdout.write(self.style.ERROR(f"Row data: \n{row}"))

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
            self.stdout.write(self.style.ERROR(f"Error loading data: {e}"))

    def load_data(self, filepath: str, sheet_name: str):
        try:
            self.stdout.write(
                self.style.SUCCESS(f"Loading data from {filepath} sheet {sheet_name}")
            )
            xls = pd.ExcelFile(filepath)

            if sheet_name:
                df = pd.read_excel(xls, sheet_name, header=1)
                df = df.replace({np.nan: None})
                df.columns = (
                    df.columns.str.strip()
                    .str.lower()
                    .str.replace("[^\w\s]", "")
                    .str.replace(" ", "_")
                )
                dfs = {sheet_name: df}
            else:
                dfs = pd.read_excel(xls, sheet_name=None, header=1)
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
                    try:
                        library = row.get("library")
                        editorial_status = row.get("editorial_status")
                        reference = row.get("reference")
                        codex = row.get("codex")
                        text_decoration = row.get("text_decoration")
                        detail = row.get("detail")
                        viewer_note = row.get("viewer_note")

                        manuscript = SingleManuscript(
                            library=Library.objects.get(library=library),
                            editorial_status=EditorialStatus.objects.get(
                                siglum=editorial_status
                            ),
                            reference=Reference.objects.get(reference=reference),
                            codex=Codex.objects.get(id=codex),
                            text_decoration=TextDecoration.objects.get(
                                text_decoration=text_decoration
                            ),
                            detail=Detail.objects.get(detail=detail),
                            viewer_note=ViewerNote.objects.get(viewer_note=viewer_note),
                        )
                        manuscript.save()
                    except Exception as e:
                        self.handle_error(index, e, row, "library", row.get("library"))
                        continue
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error loading data: {e}"))
            raise e
