from django.db import models


class Game(models.Model):
    name = models.CharField(max_length=255)
    token = models.CharField(unique=True, max_length=255)


class Map(models.Model):
    game = models.OneToOneField(Game, on_delete=models.CASCADE, related_name="map")
    image = models.ImageField(upload_to='upload/')
    width = models.PositiveIntegerField()
    height = models.PositiveIntegerField()


class Blob(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="blobs")
    x = models.PositiveSmallIntegerField()
    y = models.PositiveSmallIntegerField()
