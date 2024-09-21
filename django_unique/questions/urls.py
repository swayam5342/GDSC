from django.contrib import admin
from django.urls import path, include
from questions import views

urlpatterns = [
    path('', views.home, name="home"),
    path('questions', views.questions, name="questions"),
    path('about', views.about, name="about"),
    path('signup', views.signup, name="signup")
]
