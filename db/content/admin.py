from django.contrib import admin
from wq.db.patterns import admin as patterns
from wq.db.patterns.models import RelationshipType, Authority
from wq.db.contrib.files.admin import FileAdmin

from .models import Page, Paper, PDF, Project, Doc, Chapter, ScreenShot, Link, LinkType, Tag, TagType, MarkdownType


class ScreenShotInline(admin.TabularInline):
    model = ScreenShot

class LinkInline(admin.TabularInline):
    model = Link

class ProjectAdmin(patterns.IdentifiedModelAdmin):
    list_filter = (
        "public",
    )

    inlines = (
        patterns.IdentifiedModelAdmin.inlines +
        patterns.RelatedModelAdmin.inlines + 
        [ScreenShotInline, LinkInline]
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

class TagInline(admin.TabularInline):
    model = Tag

class TagTypeAdmin(admin.ModelAdmin):
    inlines = [TagInline]


admin.site.register(Page, patterns.IdentifiedModelAdmin)
admin.site.register(Paper, patterns.IdentifiedModelAdmin)
admin.site.register(PDF, FileAdmin)
admin.site.register(RelationshipType)
admin.site.register(Authority, patterns.AuthorityAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Doc, DocAdmin)
admin.site.register(Chapter)
admin.site.register(TagType, TagTypeAdmin)
admin.site.register(LinkType)
admin.site.register(MarkdownType)
