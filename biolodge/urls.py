from django.conf.urls import include
from django.conf.urls import url
from django.contrib.gis import admin

from birds.views import BirdDetailAPIView
from birds.views import BirdDetailView
from birds.views import BirdListAPIView
from birds.views import BirdListView


urlpatterns = [
    url(r'^$', BirdListView.as_view()),
    url(r'^api/birds/(?P<pks>[\d,]+)/$', BirdDetailAPIView.as_view()),
    url(r'^api/birds/select/(?P<coords>[\f,]+)/$', BirdSelectionAPIView.as_view()),
    url(r'^birds/(?P<pks>[\d,]+)/$', BirdDetailView.as_view()),
    url(r'^api/birds/$', BirdListAPIView.as_view()),
    url(r'^birds/$', BirdListView.as_view(), name='bird_list'),
    url(r'^admin/', include(admin.site.urls)),
]
