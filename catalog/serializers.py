from rest_framework import serializers

from catalog.models import Game, Genre, Hub


class HubBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hub
        fields = ["id", "name"]


class GenreBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ["id", "name"]


class HubSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hub
        fields = ["id", "name", "address", "phone", "description"]


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ["id", "name", "description"]


class GameListSerializer(serializers.ModelSerializer):
    hub = HubBriefSerializer(read_only=True)

    class Meta:
        model = Game
        fields = [
            "id",
            "title",
            "rental_price_per_day",
            "rating",
            "min_players",
            "max_players",
            "complexity",
            "hub",
        ]


class GameDetailSerializer(serializers.ModelSerializer):
    hub = HubBriefSerializer(read_only=True)
    genres = GenreBriefSerializer(many=True, read_only=True)

    class Meta:
        model = Game
        fields = [
            "id",
            "title",
            "description",
            "rental_price_per_day",
            "play_time_mins",
            "min_players",
            "max_players",
            "complexity",
            "rating",
            "hub",
            "genres",
        ]


class GameWriteSerializer(serializers.ModelSerializer):
    hub_id = serializers.PrimaryKeyRelatedField(
        source="hub", queryset=Hub.objects.all()
    )
    genre_ids = serializers.PrimaryKeyRelatedField(
        source="genres",
        queryset=Genre.objects.all(),
        many=True,
        required=False,
    )

    class Meta:
        model = Game
        fields = [
            "title",
            "description",
            "rental_price_per_day",
            "play_time_mins",
            "min_players",
            "max_players",
            "complexity",
            "rating",
            "hub_id",
            "genre_ids",
        ]

    def validate(self, attrs):
        if attrs["min_players"] > attrs["max_players"]:
            raise serializers.ValidationError(
                {
                    "max_players": "Максимальна кількість гравців не може бути меншою за мінімальну."
                }
            )
        if attrs["rental_price_per_day"] < 0:
            raise serializers.ValidationError(
                {"rental_price_per_day": "Ціна оренди має бути не меншою за 0."}
            )
        if not (0 <= attrs.get("rating", 0) <= 5):
            raise serializers.ValidationError(
                {"rating": "Рейтинг має бути в межах від 0 до 5."}
            )
        return attrs
