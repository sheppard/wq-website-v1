from django.core.management.base import NoArgsCommand

from content.models import Page
import requests


README_URL = "https://raw.githubusercontent.com/wq/%s/master/README.md"
TAG_URL = "https://api.github.com/repos/wq/%s/tags"


class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        pages = Page.objects.filter(submodule=True)
        for page in pages:
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
            tag = requests.get(TAG_URL % modid).json()[0]
            commit = requests.get(tag['commit']['url']).json()['commit']
            page.latest_version = tag['name'].replace("v", "")
            page.version_date = commit['author']['date'].split("T")[0]
            page.save()
        pages.update(showcase=False)
        newest = pages.order_by('-version_date')[0]
        newest.showcase = True
        newest.save()
