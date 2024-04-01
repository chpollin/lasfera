from django.contrib import admin

from manuscript.models import (
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
    TextDecoration,
    ViewerNote,
)

# Inline models


class StanzaInline(admin.StackedInline):
    model = Stanza
    classes = ("collapse",)
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


# Custom admin models.
class SingleManuscriptAdmin(admin.ModelAdmin):
    inlines = [
        TextDecorationInline,
        ReferenceInline,
        DetailInline,
        CodexInline,
        ViewerNotesInline,
        EditorialStatusInline,
        FolioInline,
    ]
    list_display = (
        "shelfmark",
        "library",
        "manuscript_lost",
        "manuscript_destroyed",
        "id",
    )


class FolioAdmin(admin.ModelAdmin):
    inlines = [StanzaInline]


class ReferenceAdmin(admin.ModelAdmin):
    list_display = ("reference", "bert")


class LibraryAdmin(admin.ModelAdmin):
    list_display = ("library", "city", "id")


class EditorialStatusAdmin(admin.ModelAdmin):
    list_display = ("siglum", "editorial_priority", "spatial_priority")


class CodexAdmin(admin.ModelAdmin):
    list_display = ("id", "support", "height", "folia", "date")


class LocationAdmin(admin.ModelAdmin):
    inlines = [LocationAliasInline]


# Register to the admin interface.

admin.site.register(Library, LibraryAdmin)
# admin.site.register(ManuscriptLocation)
admin.site.register(EditorialStatus, EditorialStatusAdmin)
# admin.site.register(Reference, ReferenceAdmin)
# admin.site.register(Codex, CodexAdmin)
# admin.site.register(TextDecoration)
# admin.site.register(Detail)
admin.site.register(Folio, FolioAdmin)

# admin.site.register(Stanza)
admin.site.register(Location, LocationAdmin)

admin.site.register(SingleManuscript, SingleManuscriptAdmin)

# fix pluralization of codex
admin.site.site_header = "La Sfera Admin"
admin.site.site_title = "La Sfera Admin Portal"
admin.site.index_title = "Welcome to the La Sfera Manuscript Portal"
