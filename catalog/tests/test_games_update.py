"""Тести оновлення ресурсу Games.

Перевіряють PUT та PATCH /api/v1/games/{id}:
- адміністратор може повністю оновити гру (200);
- звичайний користувач отримує 403;
- неавторизований користувач отримує 401;
- 404 для неіснуючої гри;
- 400 для некоректних даних;
- 400, якщо PUT не містить усіх обов'язкових полів;
- 405, оскільки PATCH не підтримується.
"""
import pytest

pytestmark = pytest.mark.django_db

GAMES_URL = "/api/v1/games"


def game_detail_url(pk):
    return f"{GAMES_URL}/{pk}"


def test_admin_can_update_game(admin_client, game, hub, genre):
    payload = {
        "title": "Updated Game",
        "description": "Updated description",
        "rental_price_per_day": 200.0,
        "play_time_mins": 120,
        "min_players": 1,
        "max_players": 6,
        "complexity": "Hard",
        "rating": 4.9,
        "hub_id": hub.id,
        "genre_ids": [genre.id],
    }

    response = admin_client.put(game_detail_url(game.id), payload, format="json")

    assert response.status_code == 200
    game.refresh_from_db()
    assert game.title == "Updated Game"
    assert float(game.rental_price_per_day) == 200.0
    assert game.complexity == "Hard"


def test_regular_user_cannot_update_game(user_client, game, hub):
    payload = {
        "title": "Forbidden Update",
        "rental_price_per_day": 100.0,
        "play_time_mins": 60,
        "min_players": 2,
        "max_players": 4,
        "complexity": "Easy",
        "hub_id": hub.id,
    }

    response = user_client.put(game_detail_url(game.id), payload, format="json")

    assert response.status_code == 403


def test_unauthenticated_user_cannot_update_game(api_client, game, hub):
    payload = {
        "title": "Anonymous Update",
        "rental_price_per_day": 100.0,
        "play_time_mins": 60,
        "min_players": 2,
        "max_players": 4,
        "complexity": "Easy",
        "hub_id": hub.id,
    }

    response = api_client.put(game_detail_url(game.id), payload, format="json")

    assert response.status_code == 401


def test_update_missing_game_returns_404(admin_client, hub):
    payload = {
        "title": "Missing Game",
        "rental_price_per_day": 100.0,
        "play_time_mins": 60,
        "min_players": 2,
        "max_players": 4,
        "complexity": "Easy",
        "hub_id": hub.id,
    }

    response = admin_client.put(game_detail_url(999999), payload, format="json")

    assert response.status_code == 404


def test_update_game_rejects_invalid_data(admin_client, game, hub):
    payload = {
        "title": "Invalid Update",
        "rental_price_per_day": 100.0,
        "play_time_mins": 60,
        "min_players": 4,
        "max_players": 2,
        "complexity": "Easy",
        "hub_id": hub.id,
    }

    response = admin_client.put(game_detail_url(game.id), payload, format="json")

    assert response.status_code == 400


def test_update_game_requires_all_fields(admin_client, game):
    response = admin_client.put(
        game_detail_url(game.id),
        {"title": "Partial Update"},
        format="json",
    )

    assert response.status_code == 400


def test_patch_game_is_not_allowed(admin_client, game):
    response = admin_client.patch(
        game_detail_url(game.id),
        {"title": "Patched Game"},
        format="json",
    )

    assert response.status_code == 405