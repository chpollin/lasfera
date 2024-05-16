from import_export import resources

from .models import EditorialStatus, Reference, SingleManuscript


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
            "manuscript": row.get(
                "shelfmark"
            ),  # Assuming 'shelfmark' can be used to find the manuscript
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
            "manuscript": row.get(
                "shelfmark"
            ),  # Assuming 'shelfmark' can be used to find the manuscript
        }
        ed_status_instance, _ = EditorialStatus.objects.get_or_create(**ed_status)
