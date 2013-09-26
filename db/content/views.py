from wq.db.rest import views
from wq.app.util import collect
from rest_framework.response import Response
from django.conf import settings
import markdown, re

# Load documentation files from directory
def get_docs(type_id):
    return collect.readfiles(
        '%s/%s' % (settings.DOCS_ROOT, type_id),
        'md'
    ).items()

# Docs sorted by section, then title
DOC_LIST = []

# Combine documentation markdown files into a single sorted array
for section in settings.CONF['docs']:
    # Section header
    DOC_LIST.append({
        'id': section['id'],
        'type_id': section['id'],
        'label': section['label'],
        'section': True
    })

    # Documentation pages for this section
    docs = []
    for id, doc in get_docs(section['id']):
        docs.append({
            'id': id,
            'type_id': section['id'],
            'type_label': section['label'],
            'label': re.match('(.+)', doc).group(0),
            'html':  markdown.markdown(doc, settings.MARKDOWN)
        })

    # Sort alphabetically
    docs.sort(key=lambda doc: doc['id'])
    DOC_LIST.extend(docs)

# Docs indexed by id
DOCS = { doc['id']: doc for doc in DOC_LIST }

# Mimic wq.db.rest.views.ListOrCreateModelView
class DocListView(views.SimpleView):
    template_name = "doc_list.html"
    def get(self, request, *args, **kwargs):
        data = DOC_LIST
        section = request.GET.get('section', None)
        if section:
            data = [doc for doc in data if doc['type_id'] == section]
        return Response({
            'list': data
        })

# Mimic wq.db.rest.views.InstanceModelView
class DocDetailView(views.SimpleView):
    template_name = "doc_detail.html"
    def get(self, request, doc=None):
        return Response(DOCS[doc])
