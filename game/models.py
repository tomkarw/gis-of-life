import numpy as np
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from picklefield import PickledObjectField

from ai.neutral_network import NeuralNetwork
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


class Blob(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="blobs")
    x = models.PositiveSmallIntegerField()
    y = models.PositiveSmallIntegerField()
    age = models.PositiveSmallIntegerField(default=0)
    energy = models.PositiveSmallIntegerField(default=100)
    memory = models.FloatField()
    color = models.CharField(max_length=15, default="rgb(0,0,0)")
    brain = PickledObjectField()  # TODO: how to store NN state?

    def save(self, **kwargs):
        self.age = self.age or 0
        self.energy = self.energy or 100
        # TODO: process NN for storing
        self.brain = self.brain or NeuralNetwork(no_of_in_nodes=8, no_of_out_nodes=7, no_of_hidden_nodes=8)
        super().save(**kwargs)

    def act(self):
        left = self.game.map[self.x - 1][self.y]
        right = self.game.map[self.x + 1][self.y]
        top = self.game.map[self.x][self.y - 1]
        bottom = self.game.map[self.x][self.y + 1]
        input_vector = np.array([self.x, self.y, left, right, top, bottom, self.energy, self.memory])
        return self.brain.run(input_vector)

    def move(self, x, y):
        self.x = x
        self.y = y
        self.energy -= 10
        if self.energy <= 0:
            return False  # blob died from exhaustion
        return True  # blob lives

    def birth(self):
        Blob.objects.create()
        self.energy = round(0.5 * self.energy)

    def eat(self):
        self.energy = 100
