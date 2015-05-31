from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from wq.db import rest
rest.autodiscover()

from content.views import DocRedirectView
from content.models import Page, Doc
page_detail = rest.router.get_viewset_for_model(Page).as_view(
    {'get': 'retrieve'}
)
doc_detail = rest.router.get_viewset_for_model(Doc).as_view(
    {'get': 'retrieve'}
)
doc_list = rest.router.get_viewset_for_model(Doc).as_view(
    {'get': 'list'}
)

urlpatterns = patterns('',
    # Special handing for wq.* pages 
    url(r'^(?P<primary_identifiers__slug>wq\.\w+)', page_detail),

    # Versioned documentation
    url(r'^docs/(?P<doc>[^\/]+)/?$', DocRedirectView.as_view()),
    url(r'^([0-9.]+)/docs/(?P<primary_identifiers__slug>[^\/]+)/?$', doc_detail),
    url(r'^([0-9.]+)/docs/?$', doc_list),

    # Default admin and wq.db routes
    url(r'^admin/', include(admin.site.urls)),
    url(r'^generate/', include('dmt.urls')),
    url(r'^',       include(rest.router.urls)),
)
