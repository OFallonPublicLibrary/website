from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.profile_view, name='profile_view'),
    url(r'^profile_edit', views.profile_update, name='profile_edit'),
]
