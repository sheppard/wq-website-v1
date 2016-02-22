from wq.db.rest import views
from rest_framework.response import Response
from rest_framework import status
from .models import MarkdownType


# Redirect e.g. /docs/app.js to /docs/app-js
class DocRedirectView(views.SimpleView):
    template_name = "doc_detail.html"

    def get(self, request, doc=None):
        if doc.endswith('.js'):
            doc = doc.replace(".js", "-js")
        version = MarkdownType.get_default()
        response = Response({})
        response['Location'] = "/%s/docs/%s" % (version.name, doc)
        response.status_code = status.HTTP_302_FOUND
        return response


class DocViewSet(views.ModelViewSet):
    def filter_queryset(self, qs):
        section = self.request.GET.get("section", None)
        if section:
            return qs.filter(chapter_id=section)
        else:
            return super(DocViewSet, self).filter_queryset(qs)

    def list(self, request, *args, **kwargs):
        response = super(DocViewSet, self).list(request, *args, **kwargs)
        chapter = None
        rows = []
        current_version = MarkdownType.get_default()
        doc_version = getattr(
            request, 'doc_version', current_version.name,
        )
        response.data['doc_version'] = doc_version
        response.data['versions'] = [{
            'name': md.name,
            'title': md.title,
            'current': md.name == doc_version
        } for md in MarkdownType.objects.order_by('pk')]
        for row in response.data['list']:
            if row['chapter_id'] != chapter:
                rows.append({
                    'id': row['chapter_id'],
                    'type_id': row['chapter_id'],
                    'label': row['chapter_label'],
                    'chapter_id': row['chapter_id'],
                    'section': True,
                })
                chapter = row['chapter_id']
            rows.append(row)
        response.data['list'] = rows
        if "section" in request.GET:
            response['Location'] = "/chapters/%s/docs" % request.GET["section"]
            response.status_code = status.HTTP_301_MOVED_PERMANENTLY
        return response
