import pickle

from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from picklefield import PickledObjectField

from game.constants import MAP_MIN_WIDTH, MAP_MAX_WIDTH, MAP_MIN_HEIGHT, MAP_MAX_HEIGHT


class Game(models.Model):
    token = models.CharField(unique=True, max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="games")
    name = models.CharField(max_length=255)

    # map details
    image = models.ImageField(upload_to='upload/')
    map = PickledObjectField()
    width = models.PositiveIntegerField(
        validators=[
            MinValueValidator(MAP_MIN_WIDTH, message=f"Value must be between {MAP_MIN_WIDTH} and {MAP_MAX_WIDTH}"),
            MaxValueValidator(MAP_MAX_WIDTH, message=f"Value must be between {MAP_MIN_WIDTH} and {MAP_MAX_WIDTH}")
        ]
    )
    height = models.PositiveIntegerField(
        validators=[
            MinValueValidator(MAP_MIN_HEIGHT, message=f"Value must be between {MAP_MIN_HEIGHT} and {MAP_MAX_HEIGHT}"),
            MaxValueValidator(MAP_MAX_HEIGHT, message=f"Value must be between {MAP_MIN_HEIGHT} and {MAP_MAX_HEIGHT}")
        ]
    )

    def get_map(self):
        return pickle.loads(self.map)


class Blob(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="blobs")
    x = models.PositiveSmallIntegerField()
    y = models.PositiveSmallIntegerField()
    age = models.PositiveSmallIntegerField(default=0)
    energy = models.PositiveSmallIntegerField(default=100)
    memory = models.FloatField()
    color = models.CharField(max_length=15, default="rgb(0,0,0)")
    brain = PickledObjectField()
