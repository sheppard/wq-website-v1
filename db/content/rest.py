from wq.db.rest import app
from .models import Page, Paper, Example, Doc, Chapter
from .serializers import PageSerializer, DocSerializer, PaperSerializer
from .views import DocViewSet
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

app.router.register_model(
    Doc,
    queryset=Doc.objects.order_by("chapter__order", "_order"),
    serializer=DocSerializer,
    viewset=DocViewSet,
)
app.router.register_model(Chapter)

app.router.register_queryset(
    Identifier,
    Identifier.objects.exclude(content_type__model__in=['example','doc']),
)
