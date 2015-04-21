from wq.db.rest import app
from .models import Page, Paper, Example, Doc, Chapter
from .serializers import (
    PageSerializer, DocSerializer, PaperSerializer, ExampleSerializer
)
from .views import DocViewSet
from wq.db.patterns.models import Identifier, Relationship, InverseRelationship


app.router.register_model(Page, url="", serializer=PageSerializer)
app.router.register_model(Paper, url="research", serializer=PaperSerializer)


def filter_examples(qs, request):
    if request.user.is_authenticated():
        return qs.all()
    else:
        return qs.filter(public=True)

def filter_rels(qs, request):
    examples = filter_examples(Example.objects.all(), request)
    example_ids = examples.values_list('pk', flat=True)
    return (
        qs.exclude(to_content_type__model="example") |
        qs.filter(to_content_type__model="example", to_object_id__in=example_ids)
    )


app.router.register_model(
    Example,
    filter=filter_examples,
    serializer=ExampleSerializer,
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
    Identifier.objects.exclude(content_type__model__in=['example', 'doc']),
)

app.router.register_filter(Relationship, filter_rels)
app.router.register_filter(InverseRelationship, filter_rels)
