from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.views.generic.base import TemplateView

from wagtail.wagtailadmin import urls as wagtailadmin_urls
from wagtail.wagtaildocs import urls as wagtaildocs_urls
from wagtail.wagtailcore import urls as wagtail_urls

from ofpl.search import views as search_views

admin.autodiscover()

urlpatterns = []

# Normal URL Definition
normalpatterns = [
    #url(r'^$', core_views.home, name='home'),
    url(r'^django-admin/', admin.site.urls),
]

# Auth-Related
authpatterns = [
    url(r'^accounts/', include('allauth.urls')),
    url(r'^profile/$', TemplateView.as_view(template_name='profile.html'), name='account_profile'),
]

wagtailpatterns = [
    url(r'^documents/', include(wagtaildocs_urls)),
    url(r'^admin/', include(wagtailadmin_urls)),
    url(r'^search/$', search_views.search, name='search'),
    url(r'', include(wagtail_urls)),
]

urlpatterns += normalpatterns
urlpatterns += authpatterns
urlpatterns += wagtailpatterns


# Debug Toolbar
if settings.DEBUG:
    import debug_toolbar
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
