from django.urls import path
from . import views


app_name = "app1"

urlpatterns = [
    path("register/", views.register, name='register'),
    path('user_login/', views.user_login, name="user_login"),
]