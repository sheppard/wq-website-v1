from wq.db.rest.serializers import ModelSerializer
from rest_framework.serializers import Field
from rest_framework.serializers import SerializerMethodField
import markdown
import re
from django.conf import settings

class PageSerializer(ModelSerializer):
    def get_html(self, obj):
        html = markdown.markdown(obj.markdown, settings.MARKDOWN)
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
            r'(href="http[s]?:\/\/[^wq.io])',
            r'rel="external" \1',
            html
        )
        return html

    def get_default_fields(self, *args, **kwargs):
        default_fields = super(PageSerializer, self).get_default_fields(*args, **kwargs)
        if self.context['view'].depth > 0:
            default_fields['html'] = SerializerMethodField('get_html')
        return default_fields

class PaperSerializer(ModelSerializer):
    acm_dl = Field()
    doi = Field()
    citation_date = Field()
    author_list = Field()
