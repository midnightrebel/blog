from django.urls import path

from django.urls import path, re_path

from blog.views import HomeView
from . import views
from .models import *
from .views import (
    LoginAPIView, RegistrationAPIView, UserRetrieveUpdateAPIView,LogoutView
)

app_name = 'authentication'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('login/', LoginAPIView.as_view(),name='login'),
    path('register/', RegistrationAPIView.as_view(), name='register'),
    path('user/',UserRetrieveUpdateAPIView.as_view(),name ='user'),
    path('logout/',LogoutView.as_view(),name = 'logout')
]
