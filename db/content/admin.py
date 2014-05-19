from wq.db.patterns import admin
from wq.db.patterns.models import RelationshipType, Authority
from wq.db.contrib.files.admin import FileAdmin

from .models import Page, Paper, PDF, Example, Doc, Chapter

class ExampleAdmin(admin.IdentifiedModelAdmin):
    list_filter = (
        "app_version",
        "db_version",
        "io_version",
        "vera_version",
        "api_version",
        "public",
     )

class DocAdmin(admin.IdentifiedModelAdmin):
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

admin.site.register(Page, admin.IdentifiedModelAdmin)
admin.site.register(Paper, admin.IdentifiedModelAdmin)
admin.site.register(PDF, FileAdmin)
admin.site.register(RelationshipType)
admin.site.register(Authority, admin.AuthorityAdmin)
admin.site.register(Example, ExampleAdmin)
admin.site.register(Doc, DocAdmin)
admin.site.register(Chapter)
