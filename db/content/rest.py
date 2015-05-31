from wq.db import rest
from .models import Page, Paper, Example, Doc, Chapter, MarkdownType
from .serializers import (
    PageSerializer, DocSerializer, PaperSerializer,
    ExampleSerializer, MarkdownSerializer
)
from .views import DocViewSet
from wq.db.patterns.models import (
    Identifier, Markdown, Relationship, InverseRelationship
)


rest.router.register_model(Page, url="", serializer=PageSerializer)
rest.router.register_model(Paper, url="research", serializer=PaperSerializer)


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


rest.router.register_model(
    Example,
    filter=filter_examples,
    serializer=ExampleSerializer,
)

rest.router.register_model(
    Doc,
    queryset=Doc.objects.order_by("chapter__order", "_order"),
    serializer=DocSerializer,
    viewset=DocViewSet,
)
rest.router.register_model(Chapter)
rest.router.register_model(
    MarkdownType,
    url="versions",
    queryset=MarkdownType.objects.order_by('pk')
)

rest.router.register_queryset(
    Identifier,
    Identifier.objects.exclude(content_type__model__in=['example', 'doc']),
)
rest.router.register_serializer(Markdown, MarkdownSerializer)

rest.router.register_filter(Relationship, filter_rels)
rest.router.register_filter(InverseRelationship, filter_rels)
