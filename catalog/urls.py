from django.urls import path

from catalog.views import (
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
]