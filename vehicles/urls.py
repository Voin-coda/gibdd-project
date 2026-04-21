from django.urls import path
from . import views

urlpatterns = [
    path('', views.search_vehicle, name='search_vehicle'),
    path('search/', views.search_vehicle, name='search_vehicle_page'),
    path('reports/', views.reports, name='reports'),
]