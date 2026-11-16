from django.shortcuts import get_object_or_404
from drf_spectacular.utils import OpenApiParameter, extend_schema, inline_serializer
from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from catalog.exceptions import Conflict
from catalog.models import Game, Genre, Hub
from catalog.permissions import IsAdminOrReadOnly
from catalog.serializers import (
    GameDetailSerializer,
    GameListSerializer,
    GameWriteSerializer,
    GenreSerializer,
    HubSerializer,
)

GAME_QUERY_PARAMS = [
    OpenApiParameter("search", str, description="Пошук за назвою гри."),
    OpenApiParameter("hub_id", int, description="Фільтр за ID хабу."),
    OpenApiParameter("genre_id", int, description="Фільтр за ID жанру."),
    OpenApiParameter(
        "min_players", int, description="Кількість гравців, яку підтримує гра."
    ),
    OpenApiParameter(
        "complexity",
        str,
        enum=["Easy", "Medium", "Hard"],
        description="Складність гри.",
    ),
    OpenApiParameter(
        "sort",
        str,
        enum=["price_asc", "price_desc", "rating_desc", "rating_asc", "popularity"],
        description="Сортування результатів.",
    ),
]

GameListResponse = inline_serializer(
    "GameListResponse",
    {"count": serializers.IntegerField(), "results": GameListSerializer(many=True)},
)

GameCreateResponse = inline_serializer(
    "GameCreateResponse",
    {
        "id": serializers.IntegerField(),
        "title": serializers.CharField(),
        "status": serializers.CharField(),
    },
)

ErrorResponse = inline_serializer(
    "ErrorResponse",
    {
        "error": inline_serializer(
            "ErrorBody",
            {"message": serializers.CharField(), "details": serializers.JSONField()},
        )
    },
)


class HubListCreateView(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request):
        hubs = Hub.objects.all().order_by("id")
        return Response(HubSerializer(hubs, many=True).data)

    def post(self, request):
        serializer = HubSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        hub = serializer.save()
        return Response(HubSerializer(hub).data, status=status.HTTP_201_CREATED)


class HubDetailView(APIView):
    permission_classes = [IsAdminOrReadOnly]

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
    permission_classes = [IsAdminOrReadOnly]

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


class GenreListCreateView(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request):
        genres = Genre.objects.all().order_by("id")
        return Response(GenreSerializer(genres, many=True).data)

    def post(self, request):
        serializer = GenreSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        genre = serializer.save()
        return Response(GenreSerializer(genre).data, status=status.HTTP_201_CREATED)


class GenreDetailView(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request, pk):
        genre = get_object_or_404(Genre, pk=pk)
        return Response(GenreSerializer(genre).data)

    def put(self, request, pk):
        genre = get_object_or_404(Genre, pk=pk)
        serializer = GenreSerializer(genre, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        genre = get_object_or_404(Genre, pk=pk)
        games_count = genre.games.count()
        if games_count:
            raise Conflict(
                f"Неможливо видалити жанр, оскільки за ним закріплено {games_count} ігор."
            )
        genre.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class GenreGamesView(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request, pk):
        genre = get_object_or_404(Genre, pk=pk)
        games = genre.games.all().order_by("id")
        return Response(
            {
                "genre_id": genre.id,
                "genre_name": genre.name,
                "games": [
                    {"id": game.id, "title": game.title, "rating": game.rating}
                    for game in games
                ],
            }
        )


def get_int_param(request, name):
    value = request.query_params.get(name)
    if value in (None, ""):
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        raise ValidationError({name: "Має бути цілим числом."})


SORT_MAP = {
    "price_asc": "rental_price_per_day",
    "price_desc": "-rental_price_per_day",
    "rating_desc": "-rating",
    "rating_asc": "rating",
    "popularity": "-rating",  # поля popularity немає → fallback
}


class GameListCreateView(APIView):
    permission_classes = [IsAdminOrReadOnly]

    @extend_schema(
        tags=["Games"],
        summary="Список ігор",
        description="Пошук, фільтрація та сортування. Доступний без токена.",
        parameters=GAME_QUERY_PARAMS,
        responses={200: GameListResponse, 400: ErrorResponse},
        auth=[],
    )
    def get(self, request):
        games = Game.objects.select_related("hub").prefetch_related("genres")

        search = request.query_params.get("search")
        if search:
            games = games.filter(title__icontains=search)

        hub_id = get_int_param(request, "hub_id")
        if hub_id is not None:
            games = games.filter(hub_id=hub_id)

        genre_id = get_int_param(request, "genre_id")
        if genre_id is not None:
            games = games.filter(genres__id=genre_id)

        min_players = get_int_param(request, "min_players")
        if min_players is not None:
            games = games.filter(
                min_players__lte=min_players,
                max_players__gte=min_players,
            )

        complexity = request.query_params.get("complexity")
        if complexity:
            if complexity not in Game.Complexity.values:
                raise ValidationError({"complexity": "Допустимі: Easy, Medium, Hard."})
            games = games.filter(complexity=complexity)

        sort = request.query_params.get("sort")
        if sort:
            if sort not in SORT_MAP:
                raise ValidationError({"sort": "Невідомий параметр сортування."})
            games = games.order_by(SORT_MAP[sort])
        else:
            games = games.order_by("id")

        games = games.distinct()

        return Response(
            {
                "count": games.count(),
                "results": GameListSerializer(games, many=True).data,
            }
        )

    @extend_schema(
        tags=["Games"],
        summary="Створити гру",
        description="Доступно лише адміністраторам (role='admin').",
        request=GameWriteSerializer,
        responses={
            201: GameCreateResponse,
            400: ErrorResponse,
            401: ErrorResponse,
            403: ErrorResponse,
        },
        auth=[{"jwtAuth": []}],
    )
    def post(self, request):
        serializer = GameWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        game = serializer.save()
        return Response(
            {"id": game.id, "title": game.title, "status": "created"},
            status=status.HTTP_201_CREATED,
        )


class GameDetailView(APIView):
    permission_classes = [IsAdminOrReadOnly]

    @extend_schema(
        tags=["Games"],
        summary="Деталі гри",
        responses={200: GameDetailSerializer, 404: ErrorResponse},
        auth=[],
    )
    def get(self, request, pk):
        game = get_object_or_404(
            Game.objects.select_related("hub").prefetch_related("genres"),
            pk=pk,
        )
        return Response(GameDetailSerializer(game).data)

    @extend_schema(
        tags=["Games"],
        summary="Оновити гру",
        description="Повне оновлення. Доступно лише адміністраторам (role='admin').",
        request=GameWriteSerializer,
        responses={
            200: GameDetailSerializer,
            400: ErrorResponse,
            401: ErrorResponse,
            403: ErrorResponse,
            404: ErrorResponse,
        },
        auth=[{"jwtAuth": []}],
    )
    def put(self, request, pk):
        game = get_object_or_404(Game, pk=pk)
        serializer = GameWriteSerializer(game, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(GameDetailSerializer(game).data)

    @extend_schema(
        tags=["Games"],
        summary="Видалити гру",
        description="Доступно лише адміністраторам (role='admin').",
        responses={
            204: None,
            401: ErrorResponse,
            403: ErrorResponse,
            404: ErrorResponse,
        },
        auth=[{"jwtAuth": []}],
    )
    def delete(self, request, pk):
        game = get_object_or_404(Game, pk=pk)
        game.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
