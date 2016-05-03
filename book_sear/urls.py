from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.search),
    url(r'', views.search_started, name='search_started'),
]