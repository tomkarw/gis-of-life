from random import randint, random

from ai.neutral_network import NeuralNetwork


def create_blob(game):
    from game.models import Blob
    Blob.objects.create(
        game=game,
        x=randint(0, game.width - 1),
        y=randint(0, game.height - 1),
        color=f"rgb({randint(127,255)}, {randint(127,255)}, {randint(127,255)})",
        memory=random(),
        brain=NeuralNetwork(no_of_in_nodes=8, no_of_out_nodes=7, no_of_hidden_nodes=8)
    )


def advance_frame(game):
    from game.blob import act
    map = game.get_map()
    for blob in game.blobs.all():
        if not act(blob, map):
            blob.delete()
        else:
            blob.save()
