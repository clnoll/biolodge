from django.conf.urls import include
from django.conf.urls import url
from django.contrib.gis import admin

from birds.views import BirdDetailView
from birds.views import BirdListAPIView
from birds.views import BirdListView


urlpatterns = [
    url(r'^$', BirdListView.as_view()),
    url(r'^birds/', BirdListView.as_view()),
    url(r'^birds/(?P<pk>\d+)/$', BirdDetailView.as_view()),
    url(r'^api/birds/', BirdListAPIView.as_view()),
    url(r'^admin/', include(admin.site.urls)),
]
