from django.urls import path
from . import views

app_name='calculator'

urlpatterns = [
    path('', views.home, name='home'),
    path('battery/', views.battery, name='battery'),
    path('solar/', views.solar_size, name='solar'),
    path('generator/', views.generator_size, name='generator'),
]
