from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
    path('createUser/', views.createUser),
    path('login/', views.login),
    path('books/', views.books),
]