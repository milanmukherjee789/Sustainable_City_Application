from django.urls import path
from . import views
urlpatterns = [
    # path('', views.apiOverview,name='apiOverview'),
    path('list/', views.ShowAll,name='list'),
    path('add/', views.addTweet,name='add')
]
