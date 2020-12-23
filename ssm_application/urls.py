from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('reg_user', views.register_user),
    path('log_in', views.log_in),
    path('dashboard', views.dashboard),
    path('goals', views.goals),
    path('logout', views.logout),
]