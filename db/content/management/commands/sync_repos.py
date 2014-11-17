from django.core.management.base import NoArgsCommand

from content.models import Page
import requests


README_URL = "https://raw.githubusercontent.com/wq/%s/master/README.md"
TAG_URL = "https://api.github.com/repos/wq/%s/tags"


class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        for page in Page.objects.filter(submodule=True):
            # Retrieve README from this module's repo
            modid = page.primary_identifier.slug
            readme = requests.get(README_URL % modid).text

            # Skip initial image
            if readme.startswith("[![" + modid):
                readme = "\n".join(readme.split("\n")[1:])

            # Replace links to this page with bold text
            readme = readme.replace(
                "[%s](http://wq.io/%s)" % (modid, modid),
                "**%s**" % modid
            )
            readme = readme.replace("[^1]", "<sup>1</sup>")
            page.markdown = readme

            # Retrieve last tag
            tag = requests.get(TAG_URL % modid).json()[0]['name']
            page.latest_version = tag.replace("v", "")
            page.save()
