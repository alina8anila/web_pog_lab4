"""Тести видалення ресурсу Games.

Перевіряють DELETE /api/v1/games/{id}:
- адміністратор може видалити гру (204);
- звичайний користувач отримує 403;
- неавторизований користувач отримує 401;
- 404 для неіснуючої гри.
"""

import pytest

from catalog.models import Game

pytestmark = pytest.mark.django_db

GAMES_URL = "/api/v1/games"


def game_detail_url(pk):
    return f"{GAMES_URL}/{pk}"


def test_admin_can_delete_game(admin_client, game):
    response = admin_client.delete(game_detail_url(game.id))

    assert response.status_code == 204
    assert not Game.objects.filter(pk=game.id).exists()


def test_regular_user_cannot_delete_game(user_client, game):
    response = user_client.delete(game_detail_url(game.id))

    assert response.status_code == 403


def test_unauthenticated_user_cannot_delete_game(api_client, game):
    response = api_client.delete(game_detail_url(game.id))

    assert response.status_code == 401


def test_delete_missing_game_returns_404(admin_client):
    response = admin_client.delete(game_detail_url(999999))

    assert response.status_code == 404
