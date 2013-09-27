from wq.db.rest.serializers import ModelSerializer
from wq.db.rest import app
from rest_framework.serializers import SerializerMethodField
from .models import Page
import markdown
from django.conf import settings

class PageSerializer(ModelSerializer):
    def get_html(self, obj):
        return markdown.markdown(obj.markdown, settings.MARKDOWN)

    def get_default_fields(self, *args, **kwargs):
        default_fields = super(PageSerializer, self).get_default_fields(*args, **kwargs)
        if self.context['view'].depth > 0:
            default_fields['html'] = SerializerMethodField('get_html')
        return default_fields

app.router.register_serializer(Page, PageSerializer)
