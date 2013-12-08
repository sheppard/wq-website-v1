from wq.db.patterns import models
from wq.db.contrib.files.models import File

class Page(models.IdentifiedModel):
    title = models.CharField(max_length=255)
    description = models.TextField()
    markdown = models.TextField()
    submodule = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True)

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
        ids = self.identifiers.filter(authority__name="ACM Digital Library")
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
