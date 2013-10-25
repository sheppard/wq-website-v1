from wq.db.rest import views
from wq.app.util import collect
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from django.conf import settings
import markdown, re

# Load documentation files from directory
def get_docs(type_id):
    doc_files = collect.readfiles(
        '%s/%s' % (settings.DOCS_ROOT, type_id),
        'md'
    )
    docs = []
    for id, doc in doc_files.items():
        # Googlebot doesn't like webpage URLs ending with .js
        if id.endswith('.js'):
            id = id.replace('.js', '-js')
            is_jsdoc = True
        else:
            is_jsdoc = False
        docs.append((id, doc, is_jsdoc))
    return docs

def parse(doc):
    html = markdown.markdown(doc, settings.MARKDOWN)
    html = re.sub(
        r'(<\/h1>\s*<p><a) (href="https:\/\/github.com\/[^"]+\/blob)', 
        r'\1 class="github-file" \2',
        html,
        count=1
    )
    html = re.sub(
        r'a (href="https:\/\/github.com\/[^"]+\/blob)',
        r'a class="github-src" \1',
        html
    )
    html = re.sub(
        r'(href="http[s]?:\/\/[^wq.io])',
        r'rel="external" \1',
        html
    )
    return html

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
    for id, doc, is_jsdoc in get_docs(section['id']):
        docs.append({
            'id': id,
            'is_jsdoc': is_jsdoc,
            'type_id': section['id'],
            'type_label': section['label'],
            'label': re.match('(.+)', doc).group(0),
            'html':  parse(doc)
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
        if doc not in DOCS:
            raise Http404
        return Response(DOCS[doc])

# Redirect e.g. /docs/app.js to /docs/app-js
class DocRedirectView(DocDetailView):
    def get(self, request, doc=None):
        doc = doc.replace(".js", "-js")
        response = super(DocRedirectView, self).get(request, doc)
        response['Location'] = "/docs/%s" % doc
        response.status_code = status.HTTP_301_MOVED_PERMANENTLY
        return response
