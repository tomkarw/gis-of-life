from django.urls import path

from game.views import main

urlpatterns = [
    path("<str:token>/", main, name="main"),
]
