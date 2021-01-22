from django.urls import path

from game import views, api_views

urlpatterns = [
    path("", views.GameListView.as_view(), name="game-list"),
    path("create/", views.GameCreateView.as_view(), name="game-create"),
    path("<str:token>/", views.GameDetailView.as_view(), name="game-details"),
    path("<str:token>/delete/", views.GameDeleteView.as_view(), name="game-delete"),

    path("<str:token>/map/", api_views.GameMapAPIView.as_view(), name="game-map"),
    path("<str:token>/frame/", api_views.GameFrameAPIView.as_view(), name="game-frame"),
    path("<str:token>/add-blob/", api_views.GameAddBlobAPIView.as_view(), name="game-add-blob"),
]
