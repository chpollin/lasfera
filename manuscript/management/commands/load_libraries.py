from django.core.management.base import BaseCommand, CommandParser
from django.utils.text import slugify
from manuscript.models import Library
import pandas as pd
import numpy as np
from django.db import transaction


class Command(BaseCommand):
    help_text = "Load data from an Excel file. This reads information about the libraries and imports them."

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
        # Load data from the excel file
        # Read the data from the excel file
        # Iterate over the rows and create a Library object for each row
        # Save the Library object

        try:
            self.stdout.write(
                self.style.SUCCESS(f"Loading data from {filepath} sheet {sheet_name}")
            )
            xls = pd.ExcelFile(filepath)
            df = pd.read_excel(xls, sheet_name)

            if sheet_name:
                df = pd.read_excel(xls, sheet_name, header=1)
                df = df.replace({np.nan: None})
                df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
                dfs = {sheet_name: df}
            else:
                dfs = pd.read_excel(xls, sheet_name=None, header=1)
                for sheet_name, df in dfs.items():
                    df = df.replace({np.nan: None})
                    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
                    dfs[sheet_name] = df
            
            for sheet_name, df in dfs.items():
                for index, row in df.iterrows():
                    library_city = row.get("city")
                    library_name = row.get("library")

                    try:
                        self.stdout.write(self.style.SUCCESS(f"Processing row {index + 1} of sheet {sheet_name}"))
                        library = Library.objects.get(library=library_name, city=library_city)
                    except Library.DoesNotExist:
                        library = Library(library=library_name, city=library_city)
                        library.save()
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error loading data: {e}"))


                        


