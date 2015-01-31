from wq.db.patterns import models
from wq.db.contrib.files.models import File


class BasePage(models.IdentifiedModel):
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


class Chapter(models.Model):
    id = models.CharField(primary_key=True, max_length=20)
    title = models.CharField(max_length=100)
    order = models.IntegerField()

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ["order"]


class Doc(models.LocatedModel, BasePage):
    chapter = models.ForeignKey(Chapter, null=True)
    is_jsdoc = models.BooleanField(default=False)
    interactive = models.BooleanField(default=False)
    incomplete = models.BooleanField(default=False)

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
            qs = Doc.objects.order_by("chapter__order", "_order")
            for i, doc in enumerate(qs):
                Doc._id_index[doc.id] = i
                Doc._ids[i] = doc.id

        i = Doc._id_index[self.id]
        if i + diff < 0 or i + diff == len(Doc._ids):
            return None
        return Doc.objects.get(pk=Doc._ids[i + diff])

    def __unicode__(self):
        return self.title

    class Meta:
        order_with_respect_to = "chapter"
        ordering = ["chapter__order", "_order"]


class Paper(models.IdentifiedRelatedModel):
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


class Example(BasePage):
    home_url = models.CharField(max_length=255, null=True, blank=True)
    icon_url = models.CharField(max_length=255, null=True, blank=True)
    repo_url = models.CharField(max_length=255, null=True, blank=True)
    app_url = models.CharField(max_length=255, null=True, blank=True)

    app_version = models.CharField(null=True, blank=True, max_length=8)
    db_version = models.CharField(null=True, blank=True, max_length=8)
    io_version = models.CharField(null=True, blank=True, max_length=8)
    vera_version = models.CharField(null=True, blank=True, max_length=8)
    api_version = models.CharField(null=True, blank=True, max_length=8)
    developer = models.ForeignKey("auth.User", null=True, blank=True)
    public = models.BooleanField()
