from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.views.generic.base import TemplateView

from wagtail.wagtailadmin import urls as wagtailadmin_urls
from wagtail.wagtaildocs import urls as wagtaildocs_urls
from wagtail.wagtailcore import urls as wagtail_urls

from ofpl.core import views as core_views

admin.autodiscover()

urlpatterns = []

# Debug Toolbar
if settings.DEBUG:
    import debug_toolbar
    from django.contrib.staticfiles import views as staticviews
    from django.conf.urls.static import static
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
        url(r'^static/(?P<path>.*)$', staticviews.serve),
    ]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# Normal URL Definition
normalpatterns = [
    #url(r'^$', core_views.home, name='home'),
    url(r'^admin/', admin.site.urls),
]

# Auth-Related
authpatterns = [
    url(r'^accounts/', include('allauth.urls')),
    url(r'^profile/$', TemplateView.as_view(template_name='profile.html'), name='account_profile'),
]

wagtailpatterns = [
    url(r'^documents/', include(wagtaildocs_urls)),
    url(r'^cms/', include(wagtailadmin_urls)),
    url(r'', include(wagtail_urls)),  # This must be last so that it does not override more specific regexes
]

urlpatterns += normalpatterns
urlpatterns += authpatterns
urlpatterns += wagtailpatterns

