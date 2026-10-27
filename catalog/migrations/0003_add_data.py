from decimal import Decimal

from django.db import migrations

HUBS = [
    {
        "name": "Dice & Roll Kyiv",
        "address": "вул. Хрещатик, 1",
        "phone": "+380441234567",
        "description": "Хаб у центрі Києва з великою бібліотекою настільних ігор.",
    },
    {
        "name": "Board Game Station Lviv",
        "address": "вул. Соборна, 12",
        "phone": "+380322345678",
        "description": "Затишний хаб у Львові з ігровими столами та кав'ярнею.",
    },
]

GENRES = [
    {
        "name": "Стратегії",
        "description": "Ігри, що вимагають планування, тактики та довгострокових рішень.",
    },
    {
        "name": "Кооперативні",
        "description": "Ігри, де гравці об'єднуються проти спільного супротивника.",
    },
    {
        "name": "Сімейні",
        "description": "Легкі та доступні ігри для компанії будь-якого віку.",
    },
]

GAMES = [
    {
        "title": "Catan",
        "description": "Класична стратегія про освоєння острова, торгівлю ресурсами та будівництво поселень.",
        "rental_price_per_day": Decimal("150.00"),
        "play_time_mins": 90,
        "min_players": 3,
        "max_players": 4,
        "complexity": "Medium",
        "rating": Decimal("4.8"),
        "hub": "Dice & Roll Kyiv",
        "genres": ["Стратегії", "Сімейні"],
    },
    {
        "title": "Carcassonne",
        "description": "Гра з висновуванням тайлів, де гравці будують середньовічне місто.",
        "rental_price_per_day": Decimal("120.00"),
        "play_time_mins": 45,
        "min_players": 2,
        "max_players": 5,
        "complexity": "Easy",
        "rating": Decimal("4.6"),
        "hub": "Dice & Roll Kyiv",
        "genres": ["Стратегії", "Сімейні"],
    },
    {
        "title": "Pandemic",
        "description": "Кооперативна гра, у якій команда лікарів стримує глобальні спалахи хвороб.",
        "rental_price_per_day": Decimal("140.00"),
        "play_time_mins": 60,
        "min_players": 2,
        "max_players": 4,
        "complexity": "Medium",
        "rating": Decimal("4.7"),
        "hub": "Board Game Station Lviv",
        "genres": ["Кооперативні"],
    },
    {
        "title": "Ticket to Ride",
        "description": "Сімейна гра про прокладання залізничних маршрутів між містами.",
        "rental_price_per_day": Decimal("130.00"),
        "play_time_mins": 60,
        "min_players": 2,
        "max_players": 5,
        "complexity": "Medium",
        "rating": Decimal("4.5"),
        "hub": "Board Game Station Lviv",
        "genres": ["Стратегії", "Сімейні"],
    },
    {
        "title": "Gloomhaven",
        "description": "Велика кооперативна кампанія з тактичними боями та розвитком персонажів.",
        "rental_price_per_day": Decimal("250.00"),
        "play_time_mins": 120,
        "min_players": 1,
        "max_players": 4,
        "complexity": "Hard",
        "rating": Decimal("4.9"),
        "hub": "Board Game Station Lviv",
        "genres": ["Стратегії", "Кооперативні"],
    },
]


def seed_catalog(apps, schema_editor):
    Hub = apps.get_model("catalog", "Hub")
    Genre = apps.get_model("catalog", "Genre")
    Game = apps.get_model("catalog", "Game")

    hubs = {}
    for data in HUBS:
        hub, _ = Hub.objects.get_or_create(
            name=data["name"],
            defaults={
                "address": data["address"],
                "phone": data["phone"],
                "description": data["description"],
            },
        )
        hubs[hub.name] = hub

    genres = {}
    for data in GENRES:
        genre, _ = Genre.objects.get_or_create(
            name=data["name"],
            defaults={"description": data["description"]},
        )
        genres[genre.name] = genre

    for data in GAMES:
        game, _ = Game.objects.get_or_create(
            title=data["title"],
            defaults={
                "description": data["description"],
                "rental_price_per_day": data["rental_price_per_day"],
                "play_time_mins": data["play_time_mins"],
                "min_players": data["min_players"],
                "max_players": data["max_players"],
                "complexity": data["complexity"],
                "rating": data["rating"],
                "hub": hubs[data["hub"]],
            },
        )
        game.genres.set([genres[name] for name in data["genres"]])


def unseed_catalog(apps, schema_editor):
    Hub = apps.get_model("catalog", "Hub")
    Genre = apps.get_model("catalog", "Genre")
    Game = apps.get_model("catalog", "Game")

    Game.objects.filter(title__in=[item["title"] for item in GAMES]).delete()
    Genre.objects.filter(name__in=[item["name"] for item in GENRES]).delete()
    Hub.objects.filter(name__in=[item["name"] for item in HUBS]).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("catalog", "0002_game_rating"),
    ]

    operations = [
        migrations.RunPython(seed_catalog, unseed_catalog),
    ]