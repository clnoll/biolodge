from django.conf.urls import include
from django.conf.urls import url
from django.contrib.gis import admin

from birds import views


urlpatterns = [
    url(r'^$', views.BirdListView.as_view()),
    url(r'^api/birds/(?P<pks>[\d,]+)/$', views.BirdDetailAPIViewAST.as_view(), name='birds_geojson'),
    url(r'^birds/(?P<pks>[\d,]+)/$', views.BirdDetailViewAST.as_view()),
    url(r'^api/birds/$', views.BirdListAPIView.as_view()),
    url(r'^api/range/(?P<pk>\d+)/$', views.BirdRangeAPIViewAST.as_view()),
    url(r'^birds/$', views.BirdListView.as_view(), name='bird_list'),
    url(r'^world_borders/$', views.WorldBordersView.as_view()),
    url(r'^admin/', include(admin.site.urls)),
]
