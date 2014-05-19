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


class Chapter(models.Model):
    id = models.CharField(primary_key=True, max_length=20)
    title = models.CharField(max_length=100)
    order = models.IntegerField()

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ["order"]


class Doc(BasePage):
    chapter = models.ForeignKey(Chapter, null=True)
    is_jsdoc = models.BooleanField(default=False)
    interactive = models.BooleanField(default=False)

    def __unicode__(self):
        return self.title

    class Meta:
        order_with_respect_to = "chapter"
        ordering = ["chapter__order", "_order"]


class Paper(models.IdentifiedRelatedModel):
    short_title = models.CharField(max_length=40)
    full_title  = models.CharField(max_length=255)
    description = models.TextField()
    abstract    = models.TextField()

    authors     = models.CharField(max_length=255)
    conference  = models.CharField(max_length=255)
    conference_url = models.URLField(null=True)
    date        = models.DateField(null=True)

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
