from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('choose-type/', views.choose_type, name='choose_type'),
    path('choose-category/', views.choose_category, name='choose_category'),
    path('login/', views.admin_login, name='admin_login'),
]
