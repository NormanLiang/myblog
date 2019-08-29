from django.urls import path
from . import views

app_name = 'userprofile'

urlpatterns = [
    path('login/', views.User_login, name='login'),
    path('logout/', views.User_logout, name='logout'),
    path('register/', views.User_register, name='register'),
    path('delete/<int:id>', views.User_delete, name='delete'),
]