from wq.db.patterns import models
from wq.db.contrib.files.models import File

class Page(models.IdentifiedModel):
    title = models.CharField(max_length=255)
    description = models.TextField()
    markdown = models.TextField()
    submodule = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True)

    slug = ""

class Paper(models.IdentifiedRelatedModel):
    short_title = models.CharField(max_length=40)
    full_title  = models.CharField(max_length=255)
    description = models.TextField()
    abstract    = models.TextField()

    authors     = models.CharField(max_length=255)
    conference  = models.CharField(max_length=255)
    conference_url = models.URLField(null=True)
    date        = models.DateField(null=True)

    slug        = "research"

class PDF(File):
    type_name = "Paper"
    def get_directory(self):
        return "papers"
    class Meta:
        proxy = True
