from django.urls import path
from . import views

app_name = 'admins'

urlpatterns = [
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('logout/', views.admin_logout, name='admin_logout'),
    path('access-list/', views.access_list, name='access_list'),
    path('user-list/', views.user_list, name='user_list'),
    path('archive-list/', views.archive_list, name='archive_list'),
    path('host-list/', views.host_list, name='host_list'),
]