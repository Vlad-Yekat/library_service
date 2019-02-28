""" Для определения URL-ов приложения """
from django.urls import path

from . import views

urlpatterns = [path("", views.index, name="index")]
