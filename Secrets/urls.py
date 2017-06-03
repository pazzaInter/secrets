from django.conf.urls import url, include

urlpatterns = [
    url(r'^', include('apps.login.urls', namespace='login')),
    url(r'^secrets/', include('apps.secrets.urls', namespace='secrets')),
]
