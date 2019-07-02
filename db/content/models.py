from django.db import models
from wq.db.patterns import models as patterns
from wq.db.contrib.files.models import File, BaseFile

from django.utils.functional import cached_property

class BasePage(patterns.IdentifiedRelatedModel):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    markdown = models.TextField(null=True, blank=True)
    updated = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True


class Page(BasePage):
    submodule = models.BooleanField(default=False)
    latest_version = models.CharField(null=True, blank=True, max_length=8)
    version_date = models.DateField(null=True, blank=True)
    showcase = models.BooleanField(default=False)


class Chapter(patterns.RelatedModel):
    id = models.CharField(primary_key=True, max_length=20)
    title = models.CharField(max_length=100)
    order = models.IntegerField()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["order"]


class Doc(patterns.LocatedModel, patterns.IdentifiedMarkedModel, patterns.RelatedModel):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    updated = models.DateTimeField(null=True, blank=True)
    chapter = models.ForeignKey(Chapter, null=True)
    is_jsdoc = models.BooleanField(default=False)
    interactive = models.BooleanField(default=False)
    incomplete = models.BooleanField(default=False)
    indent = models.BooleanField(default=False)
    referral = models.BooleanField(default=False)
    image = models.TextField(max_length=255, null=True, blank=True)
    removed = models.BooleanField(default=False)

    @property
    def next(self):
        return self.get_adjacent_doc(+1)

    @property
    def prev(self):
        return self.get_adjacent_doc(-1)

    def get_adjacent_doc(self, diff):
        if not hasattr(Doc, "_id_index"):
            Doc._id_index = {}
            Doc._ids = {}
            qs = Doc.objects.exclude(
                removed=True
            ).order_by("chapter__order", "_order")
            for i, doc in enumerate(qs):
                Doc._id_index[doc.id] = i
                Doc._ids[i] = doc.id

        if self.id not in Doc._id_index:
            return None
        i = Doc._id_index[self.id]
        if i + diff < 0 or i + diff == len(Doc._ids):
            return None
        if i + diff in Doc._ids:
            return Doc.objects.get(pk=Doc._ids[i + diff])
        else:
            return None

    def __str__(self):
        return self.title

    class Meta:
        order_with_respect_to = "chapter"
        ordering = ["chapter__order", "_order"]


class Paper(patterns.IdentifiedRelatedModel):
    short_title = models.CharField(max_length=40)
    full_title = models.CharField(max_length=255)
    description = models.TextField()
    abstract = models.TextField()

    authors = models.CharField(max_length=255)
    conference = models.CharField(max_length=255)
    conference_url = models.URLField(null=True)
    date = models.DateField(null=True)

    conference_longname = models.CharField(max_length=255)
    publisher = models.CharField(max_length=255)

    @property
    def author_list(self):
        return self.authors.split(', ')

    @property
    def citation_date(self):
        return self.date.strftime('%Y/%m/%d')

    @property
    def doi(self):
        ids = self.identifiers.filter(authority__name="DOI")
        if ids:
            return ids[0].name
        else:
            return None

    @property
    def acm_dl(self):
        ids = self.identifiers.filter(authority__name__contains="ACM")
        if ids:
            return ids[0].url
        else:
            return None

    class Meta:
        ordering = ["-date"]


class PDF(File):
    type_name = "Paper"

    def get_directory(self):
        return "papers"

    class Meta:
        proxy = True


class Project(BasePage):
    icon = models.ImageField(null=True, blank=True, upload_to="icons")

    developer = models.ForeignKey("auth.User", null=True, blank=True)
    public = models.BooleanField()

    tags = models.ManyToManyField("Tag")

    @cached_property
    def modules(self):
        pages = Page.objects.filter_by_related(self, inverse=True)
        pages = pages.filter(submodule=True)
        return [
            page.primary_identifier.slug
            for page in pages
        ]

    @property
    def full_api(self):
        return ("wq.db" in self.modules and "wq.app" in self.modules)


class LinkType(models.Model):
    name = models.CharField(max_length=255)
    icon = models.ImageField(null=True, blank=True, upload_to="icons")
     
    def __str__(self):
        return self.name

    class Meta:
        ordering = ('pk',)


class Link(models.Model):
    project = models.ForeignKey(Project)
    type = models.ForeignKey(LinkType)
    url = models.URLField()

    @property
    def icon(self):
        if self.type.icon:
            return self.type.icon.name
        return None

    def __str__(self):
        return self.type.name

    class Meta:
        ordering = ('type_id',)


class TagType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('pk',)

class Tag(models.Model):
    type = models.ForeignKey(TagType)
    name = models.CharField(max_length=255)

    def __str__(self):
        return "%s: %s" % (self.type.name, self.name)

    class Meta:
        ordering = ('type_id',)

class ScreenShot(BaseFile):
    project = models.ForeignKey(Project)

    def get_directory(self):
        return "screenshots"

    class Meta:
        ordering = ('pk',)


class MarkdownType(patterns.BaseMarkdownType):
    title = models.CharField(max_length=100)
    doc_branch = models.CharField(max_length=50)
    app_branch = models.CharField(max_length=50)
    db_branch = models.CharField(max_length=50)
    io_branch = models.CharField(max_length=50)
    current = models.BooleanField(default=False)
    deprecated = models.BooleanField(default=False)

    @classmethod
    def get_current_filter(self, request):
        return {'name': getattr(request, 'doc_version', '-1')}

    @classmethod
    def get_default(cls):
        return cls.objects.get(current=True)

    class Meta:
        ordering = ['-pk']
