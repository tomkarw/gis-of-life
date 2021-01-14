from random import randint, random

from ai.neutral_network import NeuralNetwork


def create_blob(game):
    from game.models import Blob
    Blob.objects.create(
        game=game,
        x=randint(0, game.width),
        y=randint(0, game.height),
        color=f"rgb({randint(0,255)}, {randint(0,255)}, {randint(0,255)})",
        memory=random(),
        brain=NeuralNetwork(no_of_in_nodes=8, no_of_out_nodes=7, no_of_hidden_nodes=8)
    )


def advance_frame(game):
    from game.blob import act
    map = game.get_map()
    for blob in game.blobs.all():
        act(blob, map)
        blob.save()
