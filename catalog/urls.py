from django.urls import path

from catalog.views import HubDetailView, HubGamesView, HubListCreateView

urlpatterns = [
    #path("hubs", HubListCreateView.as_view()),
    #path("hubs/<int:pk>", HubDetailView.as_view()),
    #path("hubs/<int:pk>/games", HubGamesView.as_view()),
]