from rest_framework import serializers
from wq.db.rest.serializers import ModelSerializer
from wq.db.patterns import serializers as patterns
import markdown
import re
from django.conf import settings
from .models import ScreenShot

SUFFIX = {
    1: "st",
    2: "nd",
    3: "rd",
}


def update_links(html, version=None):
    html = re.sub(
        r'(<\/h1>\s*<p><a) (href="https:\/\/github.com\/[^"]+\/blob)',
        r'\1 class="github-file" \2',
        html,
        count=1
    )
    html = re.sub(
        r'a (href="https:\/\/github.com\/[^"]+\/blob)',
        r'a class="github-src" \1',
        html
    )
    html = re.sub(
        r'(href="http[s]?:\/\/(?!wq\.io))',
        r'rel="external" \1',
        html
    )
    if version:
        for mod in ('app', 'db', 'io'):
            url =  "https://github.com/wq/wq.%s/blob/" % mod
            branch = getattr(version, mod + '_branch')
            html = html.replace(url + "master", url + branch) 

        html = re.sub(
            r'https?:\/\/wq.io\/(docs\/[^"]+)',
            r'https://wq.io/' + version.name  + r'/\1',
            html
        )
    return html


class PageSerializer(patterns.IdentifiedModelSerializer):
    version_date_label = serializers.SerializerMethodField("get_version_date")
    html = serializers.SerializerMethodField()

    def get_html(self, obj):
        html = markdown.markdown(obj.markdown, settings.MARKDOWN_EXTENSIONS)
        return update_links(html)

    def get_version_date(self, obj):
        if not getattr(obj, 'version_date', None):
            return None
        date = obj.version_date.strftime('%B %d, %Y')
        date = date.replace(" 0", " ")
        sfx = SUFFIX.get(obj.version_date.day % 10, 'th')
        date = date.replace(",", sfx + ",")
        return date

    class Meta(patterns.IdentifiedModelSerializer.Meta):
        list_exclude = (
            patterns.IdentifiedModelSerializer.Meta.list_exclude + ('html',)
        )


class MarkdownSerializer(patterns.MarkdownSerializer):
    html = serializers.SerializerMethodField()
    def get_html(self, instance):
        return update_links(instance.html, instance.type)


class DocSerializer(patterns.IdentifiedMarkedModelSerializer):
    next_id = serializers.SerializerMethodField()
    next_label = serializers.SerializerMethodField()
    prev_id = serializers.SerializerMethodField()
    prev_label = serializers.SerializerMethodField()
    versions = serializers.SerializerMethodField()

    markdown = MarkdownSerializer(many=True)

    def to_representation(self, obj):
        data = super().to_representation(obj)
        if 'markdown' in data:
            if len(data['markdown']) == 0:
                data['markdown'] = [{
                    'not_found': True,
                    'latest_version': data['versions'][-1],
                }]
                return data
            for v in data['versions']:
                if v['name'] == data['markdown'][0]['type_label']:
                    v['current'] = True
        else:
            data['versions'][-1]['current'] = True
        return data

    def get_next_id(self, instance):
        if instance.next:
            return instance.next.primary_identifier.slug

    def get_next_label(self, instance):
        if instance.next:
            return str(instance.next)

    def get_prev_id(self, instance):
        if instance.prev:
            return instance.prev.primary_identifier.slug

    def get_prev_label(self, instance):
        if instance.prev:
            return str(instance.prev)

    def get_versions(self, instance):
        return [{
            'name': md.type.name,
            'title': md.type.title
        } for md in instance.markdown.order_by('type_id')]

class ScreenShotSerializer(ModelSerializer):
    class Meta:
        model = ScreenShot


class ExampleSerializer(PageSerializer):
    modules = serializers.ReadOnlyField()
    full_api = serializers.ReadOnlyField()
    screenshots = ScreenShotSerializer(many=True, source="screenshot_set")


class PaperSerializer(patterns.IdentifiedModelSerializer):
    acm_dl = serializers.ReadOnlyField()
    doi = serializers.ReadOnlyField()
    citation_date = serializers.ReadOnlyField()
    author_list = serializers.ReadOnlyField()
