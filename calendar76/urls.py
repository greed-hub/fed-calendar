from django.urls import path
from . import views

urlpatterns = [
    path('json', views.getJson, name = 'getJson'),
    path('', views.index, name = 'index'),
]
