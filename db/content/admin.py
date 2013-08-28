from wq.db.patterns import admin
from wq.db.patterns.models import RelationshipType, Authority
from wq.db.contrib.files.admin import FileAdmin

from .models import Page, Paper, PDF

admin.site.register(Page, admin.IdentifiedModelAdmin)
admin.site.register(Paper, admin.IdentifiedModelAdmin)
admin.site.register(PDF, FileAdmin)
admin.site.register(RelationshipType)
admin.site.register(Authority, admin.AuthorityAdmin)
