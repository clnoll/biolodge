from django.conf.urls import include
from django.conf.urls import url
from django.contrib.gis import admin

from birds.views import BirdListAPIView
from birds.views import BirdListFilter
from birds.views import BirdListView


urlpatterns = [
    url(r'^$', BirdListView.as_view()),
    url(r'^birds/search/', BirdListFilter.as_view(), name='bird_list_filter'),
    url(r'^birds/', BirdListView.as_view(), name='bird_list'),
    url(r'^api/birds/', BirdListAPIView.as_view()),
    url(r'^admin/', include(admin.site.urls)),
]
