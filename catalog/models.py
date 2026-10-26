from django.db import models


class Hub(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=32)
    description = models.TextField(blank=True, default="")

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, default="")

    def __str__(self):
        return self.name


class Game(models.Model):
    class Complexity(models.TextChoices):
        EASY = "Easy"
        MEDIUM = "Medium"
        HARD = "Hard"

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, default="")
    rental_price_per_day = models.DecimalField(max_digits=8, decimal_places=2)
    play_time_mins = models.PositiveIntegerField()
    min_players = models.PositiveIntegerField()
    max_players = models.PositiveIntegerField()
    complexity = models.CharField(max_length=10, choices=Complexity.choices)
    hub = models.ForeignKey(Hub, on_delete=models.PROTECT, related_name="games")
    genres = models.ManyToManyField(Genre, related_name="games", blank=True)

    def __str__(self):
        return self.title
    
#`Users`
#`Reviews`
#`CartItems
#`Orders`
#`OrderItems`
# ці пізніше зроблю