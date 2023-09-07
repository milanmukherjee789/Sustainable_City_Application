from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from serverApi import views

router = routers.DefaultRouter()

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('api/', include('serverApi.urls')),
# ]
urlpatterns = router.urls
urlpatterns += [
    path('admin/', admin.site.urls),
    path('list/', views.ShowAll,name='list'),
    path('add/', views.addTweet,name='add')
]