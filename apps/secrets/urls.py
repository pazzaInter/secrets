from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.welcome, name='welcome'),
    url(r'^post_secret$', views.post_secret, name='post_secret'),
    url(r'^popular$', views.popular, name='popular'),
    url(r'^(?P<id>\d+)/like$', views.like, name='like'),
    url(r'^(?P<id>\d+)/delete$', views.delete, name='delete'),
]
