from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from catalog.exceptions import Conflict
from catalog.models import Hub
from catalog.serializers import HubSerializer


class HubListCreateView(APIView):
    def get(self, request):
        hubs = Hub.objects.all().order_by("id")
        return Response(HubSerializer(hubs, many=True).data)

    def post(self, request):
        serializer = HubSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        hub = serializer.save()
        return Response(HubSerializer(hub).data, status=status.HTTP_201_CREATED)


class HubDetailView(APIView):
    def get(self, request, pk):
        hub = get_object_or_404(Hub, pk=pk)
        return Response(HubSerializer(hub).data)

    def put(self, request, pk):
        hub = get_object_or_404(Hub, pk=pk)
        serializer = HubSerializer(hub, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        hub = get_object_or_404(Hub, pk=pk)
        games_count = hub.games.count()
        if games_count:
            raise Conflict(
                f"Неможливо видалити хаб, оскільки за ним закріплено {games_count} ігор."
            )
        hub.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class HubGamesView(APIView):
    def get(self, request, pk):
        hub = get_object_or_404(Hub, pk=pk)
        games = hub.games.all().order_by("id")
        return Response(
            {
                "hub_id": hub.id,
                "hub_name": hub.name,
                "games": [
                    {
                        "id": game.id,
                        "title": game.title,
                        "rental_price_per_day": game.rental_price_per_day,
                    }
                    for game in games
                ],
            }
        )