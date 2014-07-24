from wq.db.rest import views
from rest_framework.response import Response
from rest_framework import status


# Redirect e.g. /docs/app.js to /docs/app-js
class DocRedirectView(views.SimpleView):
    template_name = "doc_detail.html"

    def get(self, request, doc=None):
        doc = doc.replace(".js", "-js")
        response = Response({})
        response['Location'] = "/docs/%s" % doc
        response.status_code = status.HTTP_301_MOVED_PERMANENTLY
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
        completed = 0
        total = len(response.data['list'])
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
            if not row['incomplete']:
                completed += 1
            rows.append(row)
        response.data['list'] = rows
        completed = int(float(completed) / total * 100)
        response.data['completed'] = completed
        if "section" in request.GET:
            response['Location'] = "/chapters/%s/docs" % request.GET["section"]
            response.status_code = status.HTTP_301_MOVED_PERMANENTLY
        return response
