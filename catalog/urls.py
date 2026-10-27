from django.urls import path

from catalog.views import (
    GameDetailView,
    GameListCreateView,
    GenreDetailView,
    GenreGamesView,
    GenreListCreateView,
    HubDetailView,
    HubGamesView,
    HubListCreateView,
)

urlpatterns = [
    path("hubs", HubListCreateView.as_view()),
    path("hubs/<int:pk>", HubDetailView.as_view()),
    path("hubs/<int:pk>/games", HubGamesView.as_view()),
    path("genres", GenreListCreateView.as_view()),
    path("genres/<int:pk>", GenreDetailView.as_view()),
    path("genres/<int:pk>/games", GenreGamesView.as_view()),
    path("games", GameListCreateView.as_view()),
    path("games/<int:pk>", GameDetailView.as_view()),
]
