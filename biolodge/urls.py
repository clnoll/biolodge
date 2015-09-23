from django.conf.urls import include
from django.conf.urls import url
from django.contrib.gis import admin

from birds.views import Birds
from birds.views import map_view
from geo.views import MapView


urlpatterns = [
    url(r'^$', Birds.as_view()),
    url(r'map/', MapView.as_view()),
    url(r'^map2/', map_view),
    url(r'^admin/', include(admin.site.urls)),
]
