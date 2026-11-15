"""Тести створення ресурсу Games.

Перевіряють POST /api/v1/games:
- адміністратор може створити гру (201);
- звичайний користувач отримує 403;
- неавторизований користувач отримує 401;
- некоректні дані повертають 400:
  min_players > max_players, від'ємна ціна, рейтинг поза межами;
- відсутні обов'язкові поля;
- неіснуючий hub_id;
- некоректна складність.
"""
import pytest

from catalog.models import Game

pytestmark = pytest.mark.django_db

GAMES_URL = "/api/v1/games"


def test_admin_can_create_game(admin_client, hub, genre):
    payload = {
        "title": "New Game",
        "description": "New game description",
        "rental_price_per_day": 150.0,
        "play_time_mins": 90,
        "min_players": 3,
        "max_players": 4,
        "complexity": "Medium",
        "rating": 4.8,
        "hub_id": hub.id,
        "genre_ids": [genre.id],
    }

    response = admin_client.post(GAMES_URL, payload, format="json")

    assert response.status_code == 201
    assert response.data["title"] == "New Game"
    assert response.data["status"] == "created"
    assert Game.objects.filter(title="New Game").exists()


def test_regular_user_cannot_create_game(user_client, hub):
    payload = {
        "title": "Forbidden Game",
        "rental_price_per_day": 100.0,
        "play_time_mins": 60,
        "min_players": 2,
        "max_players": 4,
        "complexity": "Easy",
        "hub_id": hub.id,
    }

    response = user_client.post(GAMES_URL, payload, format="json")

    assert response.status_code == 403
    assert response.data["error"]["message"] == (
        "Недостатньо прав. Ця дія доступна лише адміністраторам."
    )


def test_unauthenticated_user_cannot_create_game(api_client, hub):
    payload = {
        "title": "Anonymous Game",
        "rental_price_per_day": 100.0,
        "play_time_mins": 60,
        "min_players": 2,
        "max_players": 4,
        "complexity": "Easy",
        "hub_id": hub.id,
    }

    response = api_client.post(GAMES_URL, payload, format="json")

    assert response.status_code == 401


@pytest.mark.parametrize(
    "payload,field",
    [
        (
            {
                "title": "Bad Players",
                "rental_price_per_day": 100.0,
                "play_time_mins": 60,
                "min_players": 4,
                "max_players": 2,
                "complexity": "Easy",
            },
            "max_players",
        ),
        (
            {
                "title": "Bad Price",
                "rental_price_per_day": -1.0,
                "play_time_mins": 60,
                "min_players": 2,
                "max_players": 4,
                "complexity": "Easy",
            },
            "rental_price_per_day",
        ),
        (
            {
                "title": "Bad Rating",
                "rental_price_per_day": 100.0,
                "play_time_mins": 60,
                "min_players": 2,
                "max_players": 4,
                "complexity": "Easy",
                "rating": 6.0,
            },
            "rating",
        ),
    ],
)
def test_create_game_rejects_invalid_data(admin_client, hub, payload, field):
    data = dict(payload)
    data["hub_id"] = hub.id

    response = admin_client.post(GAMES_URL, data, format="json")

    assert response.status_code == 400
    assert field in response.data["error"]["details"]


def test_create_game_rejects_missing_required_fields(admin_client, hub):
    response = admin_client.post(GAMES_URL, {"hub_id": hub.id}, format="json")

    assert response.status_code == 400


def test_create_game_rejects_invalid_hub(admin_client):
    payload = {
        "title": "Bad Hub Game",
        "rental_price_per_day": 100.0,
        "play_time_mins": 60,
        "min_players": 2,
        "max_players": 4,
        "complexity": "Easy",
        "hub_id": 999999,
    }

    response = admin_client.post(GAMES_URL, payload, format="json")

    assert response.status_code == 400


def test_create_game_rejects_invalid_complexity(admin_client, hub):
    payload = {
        "title": "Bad Complexity Game",
        "rental_price_per_day": 100.0,
        "play_time_mins": 60,
        "min_players": 2,
        "max_players": 4,
        "complexity": "Impossible",
        "hub_id": hub.id,
    }

    response = admin_client.post(GAMES_URL, payload, format="json")

    assert response.status_code == 400