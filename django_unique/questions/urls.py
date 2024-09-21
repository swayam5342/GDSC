from django.contrib import admin
from django.urls import path, include
from questions import views

urlpatterns = [
    path('', views.home, name="home"),
    path('question1', views.question1, name="questions1"),
    path('question2', views.question2, name="questions2"),
    path('question3', views.question3, name="questions3"),
    path('question4', views.question4, name="questions4"),
    path('question5', views.question5, name="questions5"),
    path('question6', views.question6, name="questions6"),
    path('question7', views.question7, name="questions7"),
    path('question8', views.question8, name="questions8"),
    path('question9', views.question9, name="questions9"),
    path('question10', views.question10, name="questions10"),
    path('result', views.result, name="result"),
    path('about', views.about, name="about"),
    path('signup', views.signup, name="signup"),
    path('profile', views.profile, name='profile'),
    path('login/', views.user_login, name='login'),
]
