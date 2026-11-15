"""Тести читання ресурсу Games.

Перевіряють GET /api/v1/games та GET /api/v1/games/{id}:
- отримання списку ігор і кількості;
- пошук за назвою;
- фільтрацію за хабом, жанром, кількістю гравців і складністю;
- сортування за ціною;
- некоректні query-параметри (400);
- отримання деталей існуючої гри;
- 404 для неіснуючої гри.
"""

import pytest

from catalog.models import Game

pytestmark = pytest.mark.django_db

GAMES_URL = "/api/v1/games"


def game_detail_url(pk):
    return f"{GAMES_URL}/{pk}"


def test_list_games_returns_all_games(api_client, game):
    response = api_client.get(GAMES_URL)

    assert response.status_code == 200
    assert response.data["count"] == Game.objects.count()
    assert any(item["id"] == game.id for item in response.data["results"])


def test_list_games_search_filters_by_title(api_client, game, hub):
    other_game = Game.objects.create(
        title="Other Game",
        description="",
        rental_price_per_day=50,
        play_time_mins=30,
        min_players=1,
        max_players=2,
        complexity=Game.Complexity.EASY,
        rating=3.0,
        hub=hub,
    )

    response = api_client.get(GAMES_URL, {"search": "Test"})

    assert response.status_code == 200
    titles = [item["title"] for item in response.data["results"]]
    assert game.title in titles
    assert other_game.title not in titles


def test_list_games_filter_by_hub(api_client, game, hub):
    response = api_client.get(GAMES_URL, {"hub_id": hub.id})

    assert response.status_code == 200
    assert all(item["hub"]["id"] == hub.id for item in response.data["results"])
    assert any(item["id"] == game.id for item in response.data["results"])


def test_list_games_filter_by_genre(api_client, game, genre):
    response = api_client.get(GAMES_URL, {"genre_id": genre.id})

    assert response.status_code == 200
    assert any(item["id"] == game.id for item in response.data["results"])


def test_list_games_filter_by_min_players(api_client, game):
    response = api_client.get(GAMES_URL, {"min_players": 3})

    assert response.status_code == 200
    assert all(
        item["min_players"] <= 3 <= item["max_players"]
        for item in response.data["results"]
    )


def test_list_games_filter_by_complexity(api_client, game):
    response = api_client.get(GAMES_URL, {"complexity": "Medium"})

    assert response.status_code == 200
    assert all(item["complexity"] == "Medium" for item in response.data["results"])
    assert any(item["id"] == game.id for item in response.data["results"])


def test_list_games_sort_by_price_asc(api_client):
    response = api_client.get(GAMES_URL, {"sort": "price_asc"})

    assert response.status_code == 200
    prices = [item["rental_price_per_day"] for item in response.data["results"]]
    assert prices == sorted(prices)


def test_list_games_rejects_invalid_complexity(api_client):
    response = api_client.get(GAMES_URL, {"complexity": "Impossible"})

    assert response.status_code == 400
    assert response.data["error"]["message"] == "Невалідні дані."


def test_list_games_rejects_invalid_sort(api_client):
    response = api_client.get(GAMES_URL, {"sort": "unknown"})

    assert response.status_code == 400
    assert response.data["error"]["message"] == "Невалідні дані."


def test_list_games_rejects_non_integer_hub_id(api_client):
    response = api_client.get(GAMES_URL, {"hub_id": "abc"})

    assert response.status_code == 400
    assert response.data["error"]["message"] == "Невалідні дані."


def test_retrieve_game_returns_details(api_client, game, genre):
    response = api_client.get(game_detail_url(game.id))

    assert response.status_code == 200
    assert response.data["id"] == game.id
    assert response.data["title"] == game.title
    assert response.data["complexity"] == game.complexity
    assert response.data["genres"][0]["name"] == genre.name


def test_retrieve_missing_game_returns_404(api_client):
    response = api_client.get(game_detail_url(999999))

    assert response.status_code == 404
    assert response.data["error"]["message"] == "Об'єкт не знайдено."
