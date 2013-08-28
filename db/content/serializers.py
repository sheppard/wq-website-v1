from wq.db.rest.serializers import ModelSerializer
from wq.db.rest import app
from rest_framework.serializers import SerializerMethodField
from .models import Page
import markdown
from django.conf import settings

class PageSerializer(ModelSerializer):
    html = SerializerMethodField('get_html')
    def get_html(self, obj):
        return markdown.markdown(obj.markdown, settings.MARKDOWN)

app.router.register_serializer(Page, PageSerializer)
