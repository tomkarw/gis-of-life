from random import randint, random

from ai.neutral_network import NeuralNetwork


def get_random_light_color():
    return f"rgb({randint(127,255)}, {randint(127,255)}, {randint(127,255)})"


def create_blob(game):
    from game.models import Blob
    Blob.objects.create(
        game=game,
        x=randint(0, game.width - 1),
        y=randint(0, game.height - 1),
        color=get_random_light_color(),
        memory=random(),
        brain=NeuralNetwork(no_of_in_nodes=8, no_of_out_nodes=7, no_of_hidden_nodes=8)
    )


def advance_frame(game):
    from game.blob import act
    map = game.get_map()
    for blob in game.blobs.all():
        if blob.age > 50:
            blob.delete()
        elif not act(blob, map):
            blob.delete()
        else:
            blob.save()
