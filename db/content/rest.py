from wq.db import rest
from .models import Page, Paper, Project, Doc, Chapter, MarkdownType
from .serializers import (
    PageSerializer, DocSerializer, PaperSerializer,
    ProjectSerializer, MarkdownSerializer
)
from .views import DocViewSet
from wq.db.patterns.models import (
    Identifier, Markdown, Relationship, InverseRelationship
)
from django.conf import settings


rest.router.register_model(Page, url="", serializer=PageSerializer)
rest.router.register_model(Paper, url="research", serializer=PaperSerializer)


def filter_projects(qs, request):
    if request.user.is_authenticated():
        return qs.all()
    else:
        return qs.filter(public=True)

def filter_rels(qs, request):
    projects = filter_projects(Project.objects.all(), request)
    project_ids = projects.values_list('pk', flat=True)
    return (
        qs.exclude(to_content_type__model="project") |
        qs.filter(to_content_type__model="project", to_object_id__in=project_ids)
    )


rest.router.register_model(
    Project,
    filter=filter_projects,
    serializer=ProjectSerializer,
)

rest.router.register_model(
    Doc,
    queryset=Doc.objects.order_by("chapter__order", "_order"),
    serializer=DocSerializer,
    viewset=DocViewSet,
    per_page=1000,
)
rest.router.register_model(Chapter)
rest.router.register_model(
    MarkdownType,
    url="versions",
    queryset=MarkdownType.objects.order_by('pk')
)

rest.router.register_queryset(
    Identifier,
    Identifier.objects.exclude(content_type__model__in=['project', 'doc']),
)
rest.router.register_serializer(Markdown, MarkdownSerializer)
rest.router.update_config(Markdown, per_page=1000)

rest.router.register_filter(Relationship, filter_rels)
rest.router.register_filter(InverseRelationship, filter_rels)

rest.router.set_extra_config(
    mapbox_token=settings.MAPBOX_TOKEN,
)
