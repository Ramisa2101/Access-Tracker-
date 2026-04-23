from django.urls import path
from . import views

urlpatterns = [
    path('visitor-access/', views.visitor_access, name='visitor_access'),
]
