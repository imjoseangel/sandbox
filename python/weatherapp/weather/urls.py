from . import views
from django.urls import path

urlpatterns: list[object] = [
    # the path for our index view
    path('', views.index),
]
