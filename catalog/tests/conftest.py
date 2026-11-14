import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from catalog.models import Game, Genre, Hub