from datetime import datetime

import numpy as np
import pandas as pd
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand, CommandParser
from django.db import transaction
from django.utils.text import slugify

from manuscript.models import (
    Codex,
    Detail,
    EditorialStatus,
    Library,
    Reference,
    SingleManuscript,
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
                    check_item_id = self.process_field(row, "item_id", index)
                    # try:
                    #     SingleManuscript.objects.get(item_id=check_item_id)
                    #     self.stdout.write(
                    #         self.style.NOTICE(
                    #             f"Item with item_id {check_item_id} already exists, skipping"
                    #         )
                    #     )
                    # except ObjectDoesNotExist:
                    # Editorial Status fields
                    editorial_status_access = self.process_field(row, "access", index)
                    editorial_status_iiif = self.process_field(row, "iiif?", index)
                    editorial_status_priority = self.process_field(
                        row, "ed_priority", index
                    )
                    editorial_status_collated = self.process_field(
                        row, "collated?", index
                    )
                    editorial_status_spatial_priority = self.process_field(
                        row, "spatial_priority", index
                    )
                    editorial_status_data_set = self.process_field(
                        row, "data_set", index
                    )
                    editorial_status_map_group = self.process_field(
                        row, "map_group", index
                    )
                    editorial_status_decorative_group = self.process_field(
                        row, "decorative_group", index
                    )

                    # Reference fields
                    reference_bert = self.process_field(row, "bert._#", index)
                    reference_reference = self.process_field(row, "reference", index)

                    # Codex fields
                    codex_support = self.process_field(row, "support", index)
                    codex_height = self.process_field(row, "height_(cm)", index)
                    codex_date = self.process_field(row, "date", index)
                    codex_folia = self.process_field(row, "folia", index)
                    codex_lines = self.process_field(row, "lines/page", index)

                    # Text Decoration fields
                    decoration_text_script = self.process_field(
                        row, "text_script", index
                    )
                    decoration_label_script = self.process_field(
                        row, "label_script", index
                    )
                    decoration_diagrams = self.process_field(row, "diagrams?", index)
                    decoration_maps = self.process_field(row, "maps?", index)
                    deocration_white_vine_work = self.process_field(
                        row, "white_vine_work?", index
                    )
                    decoration_illumination = self.process_field(
                        row, "illumination?", index
                    )
                    decoration_other = self.process_field(row, "other?", index)
                    decoration_relative_quality = self.process_field(
                        row, "relative_quality", index
                    )

                    # Detail fields
                    detail_author_attribution = self.process_field(
                        row, "author_attribution?", index
                    )
                    detail_scribe_attribution = self.process_field(
                        row, "scribe_attribution?", index
                    )

                    decoration_book_headings = self.process_field(
                        row, "book_headings", index
                    )
                    decoration_book_initials = self.process_field(
                        row, "book_initials", index
                    )

                    decoration_stanza_headings = self.process_field(
                        row, "stanza_headings", index
                    )
                    decoration_stanza_initials = self.process_field(
                        row, "stanza_initials", index
                    )
                    decoration_stanza_initials_notes = self.process_field(
                        row, "stanza_initials", index
                    )
                    decoration_stanza_separated = self.process_field(
                        row, "stanzas_separated", index
                    )
                    decoration_stanza_ed = self.process_field(row, "stanzas_#ed", index)

                    # decoration_marginal_rubrics = row.get("marginal_rubrics")

                    decoration_filigree = self.process_field(
                        row, "pen_decor.?filigree_initials", index
                    )
                    decoration_pen_decor = self.process_field(
                        row, "pen_decor.?filigree_initials", index
                    )

                    decoration_abbreviations = self.process_field(
                        row, "abbrevi-ations", index
                    )
                    decoration_catchwords = self.process_field(
                        row, "catch-words", index
                    )
                    decoration_coat_of_arms = self.process_field(
                        row, "coat_of_arms?", index
                    )
                    decoration_distance_lines = self.process_field(
                        row, "distance_lines?", index
                    )
                    decoration_distance_numbers = self.process_field(
                        row, "distance_numbers?", index
                    )
                    decoration_is_red_sea_red = self.process_field(
                        row, "is_red_sea_red?", index
                    )
                    decoration_laiazza_on_m7 = self.process_field(
                        row, "laiazza_on_m7", index
                    )
                    decoration_map_labels = self.process_field(
                        row, "map_labels?", index
                    )
                    decoration_mabel_label = self.process_field(
                        row, "mabel_label", index
                    )
                    decoration_rhodes_status = self.process_field(
                        row, "rhodes_status", index
                    )
                    decoration_standard_water = self.process_field(
                        row, "standard_water", index
                    )
                    decoration_tabriz_present = self.process_field(
                        row, "tabriz_present?", index
                    )
                    details_diagram_sun = self.process_field(
                        row, "diagram_4_(sun)?", index
                    )
                    details_gion_in_egypt = self.process_field(
                        row, "gion_in_egypt?", index
                    )

                    # Viewer Notes fields
                    viewer_notes_date_seen = self.process_field(row, "date_seen", index)
                    viewer_notes_viewer = self.process_field(row, "viewer", index)
                    viewer_notes_notes = self.process_field(row, "notes", index)

                    # Single Manuscript
                    manuscript_siglum = self.process_field(row, "siglum", index)
                    manuscript_shelfmark = self.process_field(row, "shelfmark", index)
                    manuscript_library = self.process_field(row, "library", index)
                    manuscript_url = self.process_field(row, "digitized?", index)
                    item_id = self.process_field(row, "item_id", index)
                    # ensure manuscript_url is a URL, otherwise skip
                    if manuscript_url is not None and not manuscript_url.startswith(
                        "http"
                    ):
                        manuscript_url = None
                    try:
                        manuscript_library_obj = Library.objects.get(
                            library=manuscript_library
                        )
                    except Library.DoesNotExist:
                        manuscript_library_obj = Library(library=manuscript_library)
                        manuscript_library_obj.save()

                    except Exception as e:
                        continue  # continue to next row

                    self.stdout.write(self.style.NOTICE("Processing manuscripts:"))

                    try:
                        manuscript = SingleManuscript.objects.get(item_id=item_id)
                    except SingleManuscript.DoesNotExist:
                        manuscript = SingleManuscript(
                            siglum=manuscript_siglum,
                            item_id=item_id,
                            shelfmark=manuscript_shelfmark,
                            digitized_url=manuscript_url,
                            library=manuscript_library_obj,
                        )
                        manuscript.save()

                        # except Exception as e:
                        #     self.stdout.write(self.style.ERROR(f"Error loading data: {e}"))
                        #     raise e

                        self.stdout.write(
                            self.style.SUCCESS(
                                f"Processing Editorial Status for row {index + 1} of sheet {sheet_name}"
                            )
                        )

                        editorial_status = EditorialStatus(
                            access=editorial_status_access,
                            iiif_url=editorial_status_iiif,
                            editorial_priority=editorial_status_priority,
                            collated=editorial_status_collated,
                            spatial_priority=editorial_status_spatial_priority,
                            dataset=editorial_status_data_set,
                            map_group=editorial_status_map_group,
                            decorative_group=editorial_status_decorative_group,
                            manuscript=manuscript,
                        )
                        editorial_status.save()

                        self.stdout.write(
                            self.style.SUCCESS(
                                f"Processing Reference for row {index + 1} of sheet {sheet_name}"
                            )
                        )

                        reference = Reference(
                            bert=reference_bert,
                            reference=reference_reference,
                            manuscript=manuscript,
                        )
                        reference.save()

                        self.stdout.write(
                            self.style.SUCCESS(
                                f"Processing Codex for row {index + 1} of sheet {sheet_name}"
                            )
                        )

                        codex = Codex(
                            support=codex_support,
                            height=codex_height,
                            date=codex_date,
                            folia=codex_folia,
                            lines_per_page=codex_lines,
                            related_manuscript=manuscript,
                        )
                        codex.save()

                        self.stdout.write(
                            self.style.SUCCESS(
                                f"Processing Text Decoration for row {index + 1} of sheet {sheet_name}"
                            )
                        )

                        text_decoration = TextDecoration(
                            text_script=decoration_text_script,
                            label_script=decoration_label_script,
                            diagrams=decoration_diagrams,
                            maps=decoration_maps,
                            illumination=decoration_illumination,
                            white_vine_work=deocration_white_vine_work,
                            other=decoration_other,
                            relative_quality=decoration_relative_quality,
                            manuscript=manuscript,
                        )
                        text_decoration.save()

                        # Write Detail object
                        self.stdout.write(
                            self.style.SUCCESS(
                                f"Processing Detail for row {index + 1} of sheet {sheet_name}"
                            )
                        )

                        detail = Detail(
                            author_attribution=detail_author_attribution,
                            scribe_attribution=detail_scribe_attribution,
                            book_headings=decoration_book_headings,
                            book_initials=decoration_book_initials,
                            stanza_headings_marginal_rubrics_notes=decoration_stanza_headings,
                            stanza_initials=decoration_stanza_initials,
                            stanzas_separated=decoration_stanza_separated,
                            stanzas_ed=decoration_stanza_ed,
                            filigree=decoration_filigree,
                            abbreviations=decoration_abbreviations,
                            catchwords=decoration_catchwords,
                            mabel_label=decoration_mabel_label,
                            standard_water=decoration_standard_water,
                            is_sea_red=decoration_is_red_sea_red,
                            laiazzo=decoration_laiazza_on_m7,
                            tabriz=decoration_tabriz_present,
                            rhodes_status=decoration_rhodes_status,
                            map_labels=decoration_map_labels,
                            distance_lines=decoration_distance_lines,
                            distance_numbers=decoration_distance_numbers,
                            coat_of_arms=decoration_coat_of_arms,
                            gion_in_egypt=details_gion_in_egypt,
                            diagram_sun=details_diagram_sun,
                            manuscript=manuscript,
                        )
                        detail.save()

                    # try:
                    #     self.stdout.write(
                    #         self.style.SUCCESS(
                    #             f"Processing Viewer Notes row {index + 1} of sheet {sheet_name}"
                    #         )
                    #     )
                    #     if viewer_notes_date_seen is not None:
                    #         # Convert viewer_notes_date_seen to a string if it's a datetime object
                    #         if isinstance(viewer_notes_date_seen, datetime.datetime):
                    #             viewer_notes_date_seen = viewer_notes_date_seen.strftime('%Y-%m-%d %H:%M:%S')

                    #         # if there is a comma, there are multiple dates
                    #         if "," in viewer_notes_date_seen:
                    #             date_strings = viewer_notes_date_seen.split(",")
                    #         for date_string in date_strings:
                    #             date_seen = datetime.strptime(date_string.strip(), '%Y-%m-%d %H:%M:%S')
                    #             date_seen_obj, created = ViewerNote.objects.get_or_create(
                    #                 date=date_seen
                    #             )
                    #             try:
                    #                 viewer_note = ViewerNote.objects.get(
                    #                     viewer_initials=viewer_notes_viewer,
                    #                     notes=viewer_notes_notes,
                    #                 )
                    #             except ViewerNote.DoesNotExist:
                    #                 viewer_note = ViewerNote(
                    #                     viewer_initials=viewer_notes_viewer,
                    #                     notes=viewer_notes_notes,
                    #                 )
                    #                 viewer_note.save()
                    #             viewer_note.dates_seen.add(date_seen_obj)

                    # Now we load in the manuscript data:
                    # this will be the shelfmark CharField()
                    # any potential URL in the digitized? field of the spreadsheet
                    # the library ForeignKey()

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error loading data: {e}"))
            raise e
