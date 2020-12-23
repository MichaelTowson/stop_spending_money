from django.urls import path
from . import views

urlpatterns = [

#Render Routes
    path('', views.index),
    path('register', views.register),
    path('goals', views.goals),
    path('dashboard', views.dashboard),
    path('about', views.about)
    
#Action Routes

]