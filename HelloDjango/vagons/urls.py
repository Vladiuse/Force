from django.urls import path
from . import views

app_name = 'vagons'
urlpatterns = [
    path('', views.index, name='index'),
    path('people_count', views.people_count, name='people_count'),
]