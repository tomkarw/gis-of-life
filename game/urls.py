from django.urls import path

from game import views

urlpatterns = [
    path("", views.GameListView.as_view(), name="game-list"),
    path("create/", views.GameCreateView.as_view(), name="game-create"),
    path("<str:token>/", views.GameDetailView.as_view(), name="game-details"),
    path("<str:token>/delete/", views.GameDeleteView.as_view(), name="game-delete"),
]
