from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path('signup/', views.visitor_signup, name='visitor_signup'),
    path('returning/', views.visitor_returning, name='visitor_returning'),
    path('upload-photo/', views.upload_photo, name='upload_photo'),
    path('take-photo/', views.take_photo, name='take_photo'),
    path('returning/take-photo/', views.returning_take_photo, name='returning_take_photo'),
]