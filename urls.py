from django.urls import path
from . import views

urlpatterns = [
    path('preview/', views.print_preview, name='print_preview'),
]
