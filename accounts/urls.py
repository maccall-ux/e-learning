from django.urls import path,include
from . import views


app_name='accounts'

urlpatterns=[
    #default django authentication
    path('',include('django.contrib.auth.urls')),
    #registration
    path('register/',views.register,name='register'),
]