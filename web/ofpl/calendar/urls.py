from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<year>\d+)/$', views.index, name='index'),
    url(r'^(?P<year>\d+)/(?P<month>\d+)/$', views.index, name='index'),
    url(r'^add/$', views.add, name='add'),
    url(r'^add/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/$', views.add, name='add'),
    url(r'^batchadd/$', views.batch_add, name='batch_add'),
]
