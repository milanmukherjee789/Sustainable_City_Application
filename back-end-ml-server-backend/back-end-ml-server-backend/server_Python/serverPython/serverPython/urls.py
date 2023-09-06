from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from serverApi import views

router = routers.DefaultRouter()
urlpatterns = router.urls
urlpatterns += [
    path('admin/', admin.site.urls),
    path('tweet/', views.Tweet,name='tweet'),
    path('geojson/',views.showGeoJson,name='geo'),
    path('traffic/<str:id>/',views.returnTraffic,name='traffic'),
    path('clustercab/',views.returnClusterCab,name='clustering'),
    path('prediction/<str:id>/',views.predictionDublinBikes,name='prediction'),
]
