import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from catalog.models import Game, Genre, Hub


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user(db):
    return User.objects.create_user(
        username="regular_user",
        password="UserPass123",
        email="user@example.com",
    )


@pytest.fixture
def admin_user(db):
    return User.objects.create_superuser(
        username="admin_user",
        password="AdminPass123",
        email="admin@example.com",
    )


@pytest.fixture
def user_client(user):
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.fixture
def admin_client(admin_user):
    client = APIClient()
    client.force_authenticate(user=admin_user)
    return client


@pytest.fixture
def hub(db):
    return Hub.objects.create(
        name="Test Hub",
        address="Test address",
        phone="+380000000000",
        description="Test hub description",
    )


@pytest.fixture
def genre(db):
    return Genre.objects.create(
        name="Test Genre",
        description="Test genre description",
    )


@pytest.fixture
def game(db, hub, genre):
    game = Game.objects.create(
        title="Test Game",
        description="Test game description",
        rental_price_per_day=100,
        play_time_mins=60,
        min_players=2,
        max_players=4,
        complexity=Game.Complexity.MEDIUM,
        rating=4.5,
        hub=hub,
    )
    game.genres.add(genre)
    return game
