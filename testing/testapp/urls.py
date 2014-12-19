import os

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^ckeditor/', include('ckeditor.urls')),
    url(r'^knowledge/', include('knowledge.urls')),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': os.path.join(
                os.path.dirname(__file__), '../knowledge/static'
            ).replace('\\','/')}),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
