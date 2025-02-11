from import_export import resources, fields, widgets
from import_export.widgets import ForeignKeyWidget
from import_export.results import RowResult
from django.contrib import admin
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.db.models import Q
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)

from .models import (
    EditorialStatus,
    Reference,
    SingleManuscript,
    Folio,
    Stanza,
    Location,
    LocationAlias,
)


class FolioResource(resources.ModelResource):
    """Resource for importing Folio data with proper object logging"""

    manuscript = fields.Field(
        column_name="manuscript",
        attribute="manuscript",
        widget=ForeignKeyWidget(SingleManuscript, "siglum"),
    )

    folio = fields.Field(column_name="folio", attribute="folio_number")

    line_code_range_start = fields.Field(
        column_name="line_code_starts", attribute="line_code_range_start"
    )

    line_code_range_end = fields.Field(
        column_name="next_start_line", attribute="line_code_range_end"
    )

    class Meta:
        model = Folio
        import_id_fields = ["manuscript", "folio"]
        fields = ("manuscript", "folio", "line_code_range_start", "line_code_range_end")
        skip_unchanged = False
        report_skipped = True

    def get_instance(self, instance_loader, row):
        """Get existing instance for a row if it exists"""
        try:
            manuscript = SingleManuscript.objects.get(siglum=row["manuscript"])
            return Folio.objects.get(manuscript=manuscript, folio_number=row["folio"])
        except (SingleManuscript.DoesNotExist, Folio.DoesNotExist):
            return None

    def import_row(
        self, row, instance_loader, using_transactions=True, dry_run=False, **kwargs
    ):
        """Process a single row of folio data"""
        try:
            # Get or create the instance for diff comparison
            instance = self.get_instance(instance_loader, row)

            # Get the manuscript
            manuscript = SingleManuscript.objects.get(siglum=row["manuscript"])

            if not dry_run:
                # Create or update the folio
                folio, created = Folio.objects.update_or_create(
                    manuscript=manuscript,
                    folio_number=row["folio"],
                    defaults={
                        "line_code_range_start": row["line_code_starts"],
                        "line_code_range_end": (
                            row["next_start_line"]
                            if row.get("next_start_line")
                            and row["next_start_line"].strip() != "-"
                            else None
                        ),
                    },
                )

                # Handle stanza associations
                start_line = row["line_code_starts"]
                end_line = row["next_start_line"]

                stanza_query = Q(stanza_line_code_starts__gte=start_line)
                if end_line and end_line.strip() != "-":
                    stanza_query &= Q(stanza_line_code_starts__lt=end_line)

                stanzas = Stanza.objects.filter(stanza_query).order_by(
                    "stanza_line_code_starts"
                )

                folio.stanzas.clear()
                folio.stanzas.add(*stanzas)
            else:
                # For dry run, we still need a folio object for proper logging
                folio = instance or Folio(
                    manuscript=manuscript,
                    folio_number=row["folio"],
                    line_code_range_start=row["line_code_starts"],
                    line_code_range_end=(
                        row["next_start_line"]
                        if row.get("next_start_line")
                        and row["next_start_line"].strip() != "-"
                        else None
                    ),
                )

            # Create result with proper object information
            result = RowResult()

            if instance:
                result.import_type = RowResult.IMPORT_TYPE_UPDATE
                result.diff = [
                    f"{instance.manuscript.siglum}",
                    f"{instance.folio_number}",
                    f"{instance.line_code_range_start or ''} → {row['line_code_starts']}",
                    f"{instance.line_code_range_end or ''} → {row.get('next_start_line', '')}",
                ]
            else:
                result.import_type = RowResult.IMPORT_TYPE_NEW
                result.diff = [
                    row["manuscript"],
                    row["folio"],
                    row["line_code_starts"],
                    row.get("next_start_line", ""),
                ]

            # Set object_id and object_repr for proper logging
            result.object_id = folio.pk if not dry_run else None
            result.object_repr = str(folio)

            return result

        except Exception as e:
            logger.error(f"Error importing folio row: {str(e)}", exc_info=True)
            result = RowResult()
            result.import_type = RowResult.IMPORT_TYPE_ERROR
            result.errors.append(str(e))
            return result

    def get_diff_headers(self):
        """Define headers for the diff display"""
        return ["Manuscript", "Folio", "Start Line", "End Line"]


class SingleManuscriptResource(resources.ModelResource):
    class Meta:
        model = SingleManuscript

    def before_import_row(self, row, **kwargs):
        manuscript = {
            "shelfmark": row.get("shelfmark"),
        }
        manuscript_instance, _ = SingleManuscript.objects.get_or_create(**manuscript)


class ReferenceResource(resources.ModelResource):
    class Meta:
        model = Reference

    def before_import_row(self, row, **kwargs):
        references = {
            "bert": row.get("bert"),
            "reference": row.get("reference"),
            "manuscript": row.get("siglum"),
        }
        references_instance, _ = Reference.objects.get_or_create(**references)


class EditorialStatusResource(resources.ModelResource):
    class Meta:
        model = EditorialStatus
        import_id_fields = ["siglum"]

    def before_import_row(self, row, **kwargs):
        ed_status = {
            "siglum": row.get("siglum"),
            "editorial_priority": row.get("editorial_priority"),
            "collated": row.get("collated"),
            "manuscript": row.get("siglum"),
        }
        ed_status_instance, _ = EditorialStatus.objects.get_or_create(**ed_status)


class LocationResource(resources.ModelResource):
    """Resource for importing main Location/Toponym records"""

    placename_id = fields.Field(column_name="Place_ID", attribute="placename_id")
    name = fields.Field(column_name="HistEng_Name", attribute="name")
    place_type = fields.Field(column_name="Place_Type", attribute="place_type")
    latitude = fields.Field(
        column_name="Latitude", attribute="latitude", widget=widgets.FloatWidget()
    )
    longitude = fields.Field(
        column_name="Longitude", attribute="longitude", widget=widgets.FloatWidget()
    )
    authority_file = fields.Field(column_name="Geo_Ref", attribute="authority_file")
    modern_country = fields.Field(column_name="Country", attribute="modern_country")

    def before_import(self, dataset, using_transactions=True, dry_run=False, **kwargs):
        """Skip header row"""
        if len(dataset) > 0:
            del dataset[0]

    def after_import_row(self, row, row_result, **kwargs):
        """Create alias records for modern and ancient names if they exist"""
        if row_result.import_type in [
            row_result.IMPORT_TYPE_NEW,
            row_result.IMPORT_TYPE_UPDATE,
        ]:
            try:
                location = Location.objects.get(placename_id=row.get("Place_ID"))

                # Get the values
                modern_name = row.get("Mod_Name")
                ancient_name = row.get("Anc_Name")
                mss_name = row.get("Ex_Label")

                if modern_name:
                    LocationAlias.objects.get_or_create(
                        location=location,
                        placename_modern=modern_name,
                    )

                if ancient_name:
                    LocationAlias.objects.get_or_create(
                        location=location,
                        placename_ancient=ancient_name,
                    )

                if mss_name:
                    LocationAlias.objects.get_or_create(
                        location=location,
                        placename_from_mss=mss_name,
                    )

            except Location.DoesNotExist:
                pass
            except Exception as e:
                logger.error(
                    f"Error creating alias for {row.get('Place_ID')}: {str(e)}"
                )

    class Meta:
        model = Location
        import_id_fields = ["placename_id"]
        skip_unchanged = True
        fields = (
            "placename_id",
            "name",
            "place_type",
            "latitude",
            "longitude",
            "authority_file",
            "modern_country",
        )


class LocationAliasResource(resources.ModelResource):
    id = fields.Field(attribute="id", column_name="ID")
    location = fields.Field(
        column_name="Place_ID",
        attribute="location",
        widget=ForeignKeyWidget(Location, "placename_id"),
    )
    placename_alias = fields.Field(column_name="Label", attribute="placename_alias")

    class Meta:
        model = LocationAlias
        fields = ("id", "location", "placename_alias")

    def get_diff_headers(self):
        return ["ID", "Place_ID", "Label", "MS", "Folio"]

    def import_row(
        self, row, instance_loader, using_transactions=True, dry_run=True, **kwargs
    ):
        row_result = self.get_row_result_class()()

        try:
            if not row.get("Place_ID") or not row.get("MS"):
                row_result.import_type = row_result.IMPORT_TYPE_SKIP
                row_result.diff = [
                    row.get("ID"),
                    row.get("Place_ID"),
                    row.get("Label"),
                    row.get("MS"),
                    row.get("Folio"),
                ]
                return row_result

            if "?" in str(row.get("Place_ID", "")):
                row_result.import_type = row_result.IMPORT_TYPE_SKIP
                row_result.diff = [
                    row.get("ID"),
                    row.get("Place_ID"),
                    row.get("Label"),
                    row.get("MS"),
                    row.get("Folio"),
                ]
                return row_result

            if not dry_run:
                location, _ = Location.objects.get_or_create(
                    placename_id=row["Place_ID"],
                    defaults={"name": row.get("HistEng_Name", "")},
                )

                alias, created = LocationAlias.objects.get_or_create(
                    location=location, placename_alias=row["Label"]
                )

                manuscript = SingleManuscript.objects.get(siglum=row["MS"].strip())
                alias.manuscripts.add(manuscript)

                if row.get("Folio"):
                    folio, _ = Folio.objects.get_or_create(
                        manuscript=manuscript, folio_number=row["Folio"].strip()
                    )
                    alias.folios.add(folio)

                row_result.object_id = alias.pk
                row_result.object_repr = (
                    f"{alias.location.placename_id} - {alias.placename_alias}"
                )

            row_result.import_type = row_result.IMPORT_TYPE_NEW
            row_result.diff = [
                row.get("ID"),
                row.get("Place_ID"),
                row.get("Label"),
                row.get("MS"),
                row.get("Folio"),
            ]

        except Exception as e:
            row_result.import_type = row_result.IMPORT_TYPE_ERROR
            row_result.errors.append(str(e))
            row_result.diff = [
                row.get("ID"),
                row.get("Place_ID"),
                row.get("Label"),
                row.get("MS"),
                row.get("Folio"),
            ]

        return row_result
