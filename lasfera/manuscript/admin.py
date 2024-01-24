from django.contrib import admin
from .models import Library, ManuscriptLocation, EditorialStatus, Reference, Codex, TextDecoration, Detail, Stanza, SingleManuscript

# Inline models

class StanzaInline(admin.TabularInline):
    model = Stanza
    classes = ('collapse', )

class DetailInline(admin.StackedInline):
    model = Detail
    classes = ('collapse', )

class TextDecorationInline(admin.StackedInline):
    model = TextDecoration
    classes = ('collapse', )

class CodexInline(admin.StackedInline):
    model = Codex
    classes = ('collapse', )

class ReferenceInline(admin.StackedInline):
    model = Reference
    classes = ('collapse', )

class EditorialStatusInline(admin.StackedInline):
    model = EditorialStatus
    classes = ('collapse', )
    extra = 1

# Custom admin models.

class SingleManuscriptAdmin(admin.ModelAdmin):
    inlines = [StanzaInline, EditorialStatusInline]

# Register to the admin interface.

admin.site.register(Library)
admin.site.register(ManuscriptLocation)
admin.site.register(EditorialStatus)
admin.site.register(Reference)
admin.site.register(Codex)
admin.site.register(TextDecoration)
admin.site.register(Detail)

admin.site.register(Stanza)

admin.site.register(SingleManuscript, SingleManuscriptAdmin)

# fix pluralization of codex
admin.site.site_header = "La Sfera Admin"
admin.site.site_title = "La Sfera Admin Portal"
admin.site.index_title = "Welcome to the La Sfera Manuscript Portal"

