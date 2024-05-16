from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html, format_html_join
from import_export.admin import ImportExportModelAdmin

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
from manuscript.resources import (
    EditorialStatusResource,
    ReferenceResource,
    SingleManuscriptResource,
)


# Inline models --------------------------------------------
class StanzaInline(admin.StackedInline):
    model = Stanza
    extra = 1
    fields = (
        "stanza_line_code_starts",
        "stanza_line_code_ends",
        "stanza_text",
        "stanza_notes",
        "add_stanza_variant_link",
        "display_stanza_variants",
    )
    readonly_fields = (
        "add_stanza_variant_link",
        "display_stanza_variants",
    )

    def add_stanza_variant_link(self, obj):
        url = reverse("admin:manuscript_stanzavariant_add") + "?stanza=" + str(obj.id)
        return format_html('<a href="{}">Add Stanza Variant</a>', url)

    add_stanza_variant_link.short_description = "Add Stanza Variant"

    def display_stanza_variants(self, obj):
        variants = ["- {}".format(variant) for variant in obj.stanzavariant_set.all()]
        return format_html("<br>".join(variants))

    display_stanza_variants.short_description = "Stanza Variants"


class StanzaVariantInline(admin.StackedInline):
    model = StanzaVariant
    extra = 1


class FolioInline(admin.StackedInline):
    model = Folio
    classes = ("collapse",)
    extra = 1


class DetailInline(admin.StackedInline):
    model = Detail
    classes = ("collapse",)
    extra = 1
    max_num = 1


class TextDecorationInline(admin.StackedInline):
    model = TextDecoration
    classes = ("collapse",)
    extra = 1
    max_num = 1


class ReferenceInline(admin.StackedInline):
    model = Reference
    classes = ("collapse",)
    extra = 1


class EditorialStatusInline(admin.StackedInline):
    model = EditorialStatus
    classes = ("collapse",)
    extra = 1
    max_num = 1


class ViewerNotesInline(admin.StackedInline):
    model = ViewerNote
    classes = ("collapse",)
    extra = 1


class CodexInline(admin.StackedInline):
    model = Codex
    classes = ("collapse",)
    extra = 1
    max_num = 1


class LocationAliasInline(admin.TabularInline):
    model = LocationAlias
    extra = 1


class AuthorityFileInline(admin.TabularInline):
    model = AuthorityFile
    extra = 1


# Custom admin models --------------------------------------------
class SingleManuscriptAdmin(ImportExportModelAdmin):
    inlines = [
        AuthorityFileInline,
        TextDecorationInline,
        ReferenceInline,
        DetailInline,
        CodexInline,
        ViewerNotesInline,
        EditorialStatusInline,
        FolioInline,
    ]
    list_display = (
        "siglum",
        "shelfmark",
        "library",
        "manuscript_lost",
        "manuscript_destroyed",
        "id",
    )
    resource_class = SingleManuscriptResource

    def siglum(self, obj):
        editorial_status = obj.editorialstatus_set.first()
        if editorial_status:
            return editorial_status.siglum
        else:
            return "No siglum provided"

    siglum.short_description = "Siglum"

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "library":
            kwargs["queryset"] = Library.objects.order_by("city")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    # def get_readonly_fields(self, request, obj=None):
    #     return ['item_id'] + super().get_readonly_fields(request, obj=obj)

    # def get_fields(self, request, obj=None):
    #     fields = super().get_fields(request, obj=obj)
    #     return [field for field in fields if field != 'item_id']


class FolioAdmin(admin.ModelAdmin):
    inlines = [
        StanzaInline,
    ]

    def add_link_to_edit_stanzas(self, obj):
        url = reverse("admin:manuscript_stanza_add") + "?folio=" + str(obj.id)
        return format_html('<a href="{}">Add Stanza</a>', url)


class ReferenceAdmin(ImportExportModelAdmin):
    list_display = ("reference", "bert")
    resource_class = ReferenceResource


class LibraryAdmin(admin.ModelAdmin):
    list_display = ("library", "city", "id")


class EditorialStatusAdmin(admin.ModelAdmin):
    list_display = ("siglum", "editorial_priority", "spatial_priority")
    resource_class = EditorialStatusResource


class CodexAdmin(admin.ModelAdmin):
    list_display = ("id", "support", "height", "folia", "date")


class LocationAdmin(admin.ModelAdmin):
    inlines = [LocationAliasInline]
    list_display = ("country", "latitude", "longitude", "id")


class StanzaAdmin(admin.ModelAdmin):
    inlines = [StanzaVariantInline]


class StanzaVariantAdmin(admin.ModelAdmin):
    def get_changeform_initial_data(self, request):
        initial = super().get_changeform_initial_data(request)
        if "stanza" in request.GET:
            initial["stanza"] = request.GET["stanza"]
        return initial


# Register to the admin interface.

admin.site.register(Library, LibraryAdmin)
admin.site.register(EditorialStatus, EditorialStatusAdmin)
admin.site.register(Folio, FolioAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(SingleManuscript, SingleManuscriptAdmin)
admin.site.register(Stanza, StanzaAdmin)
admin.site.register(StanzaVariant, StanzaVariantAdmin)

# fix pluralization of codex
admin.site.site_header = "La Sfera Admin"
admin.site.site_title = "La Sfera Admin Portal"
admin.site.index_title = "Welcome to the La Sfera Manuscript Portal"
