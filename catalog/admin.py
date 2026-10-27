from django.contrib import admin
from catalog.models import Game, Genre, Hub

@admin.register(Hub)
class HubAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "address", "phone")
    search_fields = ("name", "address")


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = (
        "id", "title", "hub", "complexity", "rating", "rental_price_per_day",
    )
    list_filter = ("complexity", "hub", "genres")
    search_fields = ("title",)
    filter_horizontal = ("genres",)