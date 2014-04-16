from wq.db.rest import app
from .models import Page, Paper, Example
from .serializers import PageSerializer, PaperSerializer
from wq.db.patterns.models import Identifier


app.router.register_model(Page, url="", serializer=PageSerializer)
app.router.register_model(Paper, url="research", serializer=PaperSerializer)

def filter_examples(qs, request):
    if request.user.is_authenticated():
        return qs.all()
    else:
        return qs.filter(public=True)

app.router.register_model(
    Example,
    filter=filter_examples,
    serializer=PageSerializer,
)

app.router.register_queryset(
    Identifier,
    Identifier.objects.exclude(content_type__model='example'),
)
