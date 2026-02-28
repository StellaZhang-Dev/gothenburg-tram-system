from django.urls import path
from . import views

urlpatterns = [
    path('', views.tram_net),
    path('route/', views.find_route),
]
