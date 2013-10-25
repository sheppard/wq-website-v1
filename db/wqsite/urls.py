from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from wq.db.rest import app
app.autodiscover()
app.router.add_page('index', {'url': ''})

from content.views import DocListView, DocDetailView, DocRedirectView
from content.models import Page
page_list, page_detail = app.router.get_views_for_model(Page)

urlpatterns = patterns('',
    # Special handing for wq.* and docs/*.js pages since their slugs are 
    # technically invalid
    url(r'^(?P<slug>wq\.\w+)', page_detail),
    url(r'^docs/(?P<doc>\w+\.js)/?$', DocRedirectView.as_view()),

    # Documentation paths
    url(r'^docs/$',  DocListView.as_view()),
    url(r'^docs/(?P<doc>[^\/\?]+)/?$', DocDetailView.as_view()),

    # Default admin and wq.db routes
    url(r'^admin/', include(admin.site.urls)),
    url(r'^',       include(app.router.urls)),
)



