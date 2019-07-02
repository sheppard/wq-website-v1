from rest_framework import serializers
from wq.db.rest.serializers import ModelSerializer
from wq.db.patterns import serializers as patterns
import markdown
import re
from django.conf import settings
from .models import ScreenShot, Link

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


def update_code(html):
    if 'wq for Django' not in html:
        return html

    rows = html.split('\n')
    rowid = {}

    def section_done():
        if 'pypi_start' not in rowid or 'npm_end' not in rowid:
            return
        if 'both_start' in rowid and 'both_end' not in rowid:
            return
        start = rowid['pypi_start']
        pypi_head = rows[start]
        pypi_code = rows[start + 1:rowid['pypi_end'] + 1]
        npm_head = rows[rowid['npm_start']]
        npm_code = rows[rowid['npm_start'] + 1:rowid['npm_end'] + 1]
        if 'both_end' in rowid:
            both_code = rows[rowid['both_start']:rowid['both_end']]
            both_code[0] = both_code[0].split('>', 2)[2]
            both_code.insert(0, '')
            pypi_code_end = pypi_code[-1]
            pypi_code = pypi_code[:-1] + both_code
            if 'define(' in '\n'.join(pypi_code):
                pypi_code.append('\n});')
            pypi_code.append(pypi_code_end)
            npm_code = npm_code[:-1] + both_code + npm_code[-1:]
            end = rowid['both_end']
        else:
            end = rowid['npm_end']
        for i in range(start, end + 1):
            rows[i] = ''
        rows[start] = pypi_head
        rows[start + 1] = npm_head
        rows[start + 2] = '\n'.join(pypi_code)
        rows[start + 3] = '\n'.join(npm_code)
        def set_class(row, class_name):
            rows[start + row] = rows[start + row].replace('>', ' class="{}">'.format(class_name, 1))
        set_class(0, 'code-tab active pypi')
        set_class(1, 'code-tab npm')
        set_class(2, 'code-example active pypi')
        set_class(3, 'code-example npm')
        rowid.clear()
            
    def update_row(row, i):
        if 'wq for Django' in row:
            rowid['pypi_start'] = i
        elif 'wq for Node' in row:
            rowid['npm_start'] = i
        elif '<pre>' in row:
            if 'npm_start' in rowid and i > rowid['npm_start'] + 1:
                rowid['both_start'] = i
        elif "</pre>" in row:
            if 'both_start' in rowid:
                rowid['both_end'] = i
            elif 'npm_start' in rowid:
                rowid['npm_end'] = i
            elif 'pypi_start' in rowid:
                rowid['pypi_end'] = i
        elif row:
            section_done()
        
    for i, row in enumerate(rows):
        update_row(row, i)

    return '\n'.join(rows)


class PageSerializer(patterns.IdentifiedModelSerializer):
    version_date_label = serializers.SerializerMethodField("get_version_date")
    html = serializers.SerializerMethodField()

    def get_html(self, obj):
        html = markdown.markdown(obj.markdown, settings.MARKDOWN_EXTENSIONS)
        html = update_links(html)
        html = update_code(html)
        return html

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
        html = update_links(instance.html, instance.type)
        html = update_code(html)
        return html


class DocSerializer(patterns.IdentifiedMarkedModelSerializer, patterns.LocatedModelSerializer):
    next_id = serializers.SerializerMethodField()
    next_label = serializers.SerializerMethodField()
    prev_id = serializers.SerializerMethodField()
    prev_label = serializers.SerializerMethodField()
    versions = serializers.SerializerMethodField()

    markdown = MarkdownSerializer(many=True)

    def to_representation(self, obj):
        data = super().to_representation(obj)
        stable_version = {}
        for v in data['versions']:
            if v['stable']:
                stable_version = v
        if 'markdown' in data:
            if len(data['markdown']) == 0:
                req = self.context.get('request', None)
                doc_version = (
                     getattr(req, 'doc_version', None)
                     or stable_version['name']
                )
                data['markdown'] = [{
                    'not_found': True,
                    'type_label': doc_version,
                    'latest_version': stable_version,
                }]
                return data
            found = False
            for v in data['versions']:
                if v['name'] == data['markdown'][0]['type_label']:
                    found = True
                    v['current'] = True
                    if v['name'] > stable_version['name']:
                        data['future'] = True
            if not found:
                data['deprecated'] = True
                data['markdown'][0].pop('id')
                data['latest_version'] = stable_version
        else:
            stable_version['current'] = True
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
            'title': md.type.title,
            'stable': md.type.current,
        } for md in instance.markdown.filter(
            type__deprecated=False
        ).order_by('type_id')]


class ScreenShotSerializer(ModelSerializer):
    class Meta:
        model = ScreenShot


class LinkSerializer(ModelSerializer):
    icon = serializers.ReadOnlyField()

    class Meta:
        model = Link
        fields = ['url', 'icon']


class ProjectSerializer(PageSerializer):
    modules = serializers.ReadOnlyField()
    full_api = serializers.ReadOnlyField()
    screenshots = ScreenShotSerializer(many=True, source="screenshot_set")
    links = LinkSerializer(many=True, source="link_set")


class PaperSerializer(patterns.IdentifiedModelSerializer):
    acm_dl = serializers.ReadOnlyField()
    doi = serializers.ReadOnlyField()
    citation_date = serializers.ReadOnlyField()
    author_list = serializers.ReadOnlyField()
    pdf = serializers.SerializerMethodField()

    def get_pdf(self, instance):
        pdf = instance.relationships.first()
        return str(pdf.right)
