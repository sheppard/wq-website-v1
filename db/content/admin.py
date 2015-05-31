from django.contrib import admin
from wq.db.patterns import admin as patterns
from wq.db.patterns.models import RelationshipType, Authority
from wq.db.contrib.files.admin import FileAdmin

from .models import Page, Paper, PDF, Example, Doc, Chapter, ScreenShot


class ScreenShotInline(admin.TabularInline):
    model = ScreenShot

class ExampleAdmin(patterns.IdentifiedModelAdmin):
    list_filter = (
        "public",
    )

    inlines = (
        patterns.IdentifiedModelAdmin.inlines +
        patterns.RelatedModelAdmin.inlines + 
        [ScreenShotInline]
    )

class DocAdmin(patterns.IdentifiedMarkedModelAdmin):
    list_display = (
        "title",
        "chapter",
        "updated",
    )
    list_filter = (
        "chapter",
        "updated",
    )
    ordering = (
        "chapter__order",
        "_order",
    )

admin.site.register(Page, patterns.IdentifiedModelAdmin)
admin.site.register(Paper, patterns.IdentifiedModelAdmin)
admin.site.register(PDF, FileAdmin)
admin.site.register(RelationshipType)
admin.site.register(Authority, patterns.AuthorityAdmin)
admin.site.register(Example, ExampleAdmin)
admin.site.register(Doc, DocAdmin)
admin.site.register(Chapter)
