from django.core.management.base import BaseCommand, CommandParser
from django.utils.text import slugify
from manuscript.models import SingleManuscript, ManuscriptLocation, DateSeen, EditorialStatus, Reference, Codex, TextDecoration, Detail, ViewerNote
import pandas as pd
import numpy as np
from django.db import transaction
from datetime import datetime


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
        try:
            self.stdout.write(
                self.style.SUCCESS(f"Loading data from {filepath} sheet {sheet_name}")
            )
            xls = pd.ExcelFile(filepath)
            df = pd.read_excel(xls, sheet_name)

            if sheet_name:
                df = pd.read_excel(xls, sheet_name, header=1)
                df = df.replace({np.nan: None})
                df.columns = df.columns.str.strip().str.lower().str.replace('[^\w\s]','').str.replace(" ", "_")
                dfs = {sheet_name: df}
            else:
                dfs = pd.read_excel(xls, sheet_name=None, header=1)
                for sheet_name, df in dfs.items():
                    df = df.replace({np.nan: None})
                    df.columns = df.columns.str.strip().str.lower().str.replace('[^\w\s]','').str.replace(" ", "_")
                    dfs[sheet_name] = df
            
            # check the column names
            # for sheet_name, df in dfs.items():
            #     self.stdout.write(self.style.SUCCESS(f"Sheet {sheet_name} has the following columns: {df.columns}"))
            
            for sheet_name, df in dfs.items():
                for index, row in df.iterrows():
                    editorial_status_siglum = row.get("siglum")
                    editorial_status_access = row.get("access")
                    editorial_status_iiif = row.get("iiif?")
                    editorial_status_priority = row.get("ed_priority")
                    editorial_status_collated = row.get("collated?")
                    editorial_status_spatial_priority = row.get("spatial_priority")
                    editorial_status_data_set = row.get("data_set")
                    editorial_status_spatial_group = row.get("spatial_group")

                    reference_bert = row.get("bert._#")
                    reference_reference = row.get("reference")

                    codex_support = row.get("support")
                    codex_height = row.get("height_(cm)")
                    codex_date = row.get("date")
                    codex_folia = row.get("folia")
                    codex_lines = row.get("lines/page")

                    decoration_text_script = row.get("text_script")
                    decoration_label_script = row.get("label_script")
                    decoration_diagrams = row.get("diagrams?")
                    decoration_maps = row.get("maps?")
                    deocration_white_vine_work = row.get("white_vine_work?")
                    decoration_illumination = row.get("illumination?")
                    decoration_book_initials = row.get("book_initials")
                    decoration_stanza_headings = row.get("stanza_headings")
                    decoration_stanza_initials = row.get("stanza_initials")
                    decoration_stanza_separated = row.get("stanzas_separated")
                    decoration_stanza_ed = row.get("stanzas_ed")
                    decoration_marginal_rubrics = row.get("marginal_rubrics")
                    decoration_pen_decor = row.get("pen_decor.?filigree_initials")
                    decoration_abbreviations = row.get("abbrevi-ations")
                    decoration_catchwords = row.get("catch-words")
                    decoration_mabel_label = row.get("mabel_label")
                    decoration_standard_water = row.get("standard_water")
                    decoration_is_red_sea_red = row.get("is_red_sea_red?")
                    decoration_laiazza_on_m7 = row.get("laiazza_on_m7")
                    decoration_tabriz_present = row.get("tabriz_present?")
                    decoration_rhodes_statues = row.get("rhodes_statues")
                    decoration_map_labels = row.get("map_labels?")
                    decoration_distance_lines = row.get("distance_lines?")
                    decoration_distance_numbers = row.get("distance_numbers?")
                    decoration_coat_of_arms = row.get("coat_of_arms?")

                    viewer_notes_date_seen = row.get("date_seen")
                    # date_strings = viewer_notes_date_seen.split(',')
                    # for date_string in date_strings:
                    #     date_seen = datetime.fromisoformat(date_string.strip())
                    #     date_seen_obj, created = DateSeen.objects.get_or_create(date=date_seen)
                    #     viewer_note.dates_seen.add(date_seen_obj)
                    viewer_notes_viewer = row.get("viewer")
                    viewer_notes_notes = row.get("notes")

                    try:
                        self.stdout.write(self.style.SUCCESS(f"Processing row {index + 1} of sheet {sheet_name}"))
                        editorial_status = EditorialStatus.objects.get(siglum=editorial_status_siglum)
                    except EditorialStatus.DoesNotExist:
                        editorial_status = EditorialStatus(siglum=editorial_status_siglum, access=editorial_status_access, iiif_url=editorial_status_iiif, editorial_priority=editorial_status_priority, collated=editorial_status_collated, spatial_priority=editorial_status_spatial_priority, dataset=editorial_status_data_set, group=editorial_status_spatial_group)
                        editorial_status.save()

                    try:
                        self.stdout.write(self.style.SUCCESS(f"Processing row {index + 1} of sheet {sheet_name}"))
                        reference = Reference.objects.get(bert=reference_bert)
                    except Reference.DoesNotExist:
                        reference = Reference(bert=reference_bert, reference=reference_reference)
                        reference.save()

                    try:
                        self.stdout.write(self.style.SUCCESS(f"Processing row {index + 1} of sheet {sheet_name}"))
                        codex = Codex.objects.get(support=codex_support)
                    except Codex.DoesNotExist:
                        codex = Codex(support=codex_support, height=codex_height, date=codex_date, folia=codex_folia, lines_per_page=codex_lines)
                        codex.save()

                    try:
                        self.stdout.write(self.style.SUCCESS(f"Processing row {index + 1} of sheet {sheet_name}"))
                        text_decoration = TextDecoration.objects.get(text_script=decoration_text_script)
                    except TextDecoration.DoesNotExist:
                        text_decoration = TextDecoration(text_script=decoration_text_script, label_script=decoration_label_script, diagrams=decoration_diagrams, maps=decoration_maps, white_vine_work=deocration_white_vine_work, illumination=decoration_illumination)
                        text_decoration.save()

                    # detail 
                    # book_initials=decoration_book_initials, stanza_headings=decoration_stanza_headings, stanza_initials=decoration_stanza_initials, stanzas_separated=decoration_stanzas_separated, stanzas_ed=decoration_stanzas_ed, marginal_rubrics=decoration_marginal_rubrics, pen_decor_filigree_initials=decoration_pen_decor, abbreviations=decoration_abbreviations, catchwords=decoration_catchwords, mabel_label=decoration_mabel_label, standard_water=decoration_standard_water, is_red_sea_red=decoration_is_red_sea_red, laiazza_on_m7=decoration_laiazza_on_m7, tabriz_present=decoration_tabriz_present, rhodes_statues=decoration_rhodes_statues, map_labels=decoration_map_labels, distance_lines=decoration_distance_lines, distance_numbers=decoration_distance_numbers, coat_of_arms=decoration_coat_of_arms

                    try:
                        self.stdout.write(self.style.SUCCESS(f"Processing row {index + 1} of sheet {sheet_name}"))
                        if viewer_notes_date_seen is not None:
                            # if there is a comma, there are multiple dates
                            if ',' in viewer_notes_date_seen:
                                date_strings = viewer_notes_date_seen.split(',')
                            for date_string in date_strings:
                                date_seen = datetime.fromisoformat(date_string.strip())
                                date_seen_obj, created = DateSeen.objects.get_or_create(date=date_seen)
                                try:
                                    viewer_note = ViewerNote.objects.get(viewer_initials=viewer_notes_viewer, notes=viewer_notes_notes)
                                except ViewerNote.DoesNotExist:
                                    viewer_note = ViewerNote(viewer_initials=viewer_notes_viewer, notes=viewer_notes_notes)
                                    viewer_note.save()
                                viewer_note.dates_seen.add(date_seen_obj)
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f"Error loading data at row {index + 1}, column 'date_seen': {e}"))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error loading data: {e}"))