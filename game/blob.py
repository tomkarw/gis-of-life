from random import random

import numpy as np

from game.constants import MOVE_ENERGY_LOSS, BIRTH_THRESHOLD, FOOD_TILE, MAX_BLOB_COUNT
from game.utils import create_blob


def modulo(val, range):
    return val % (range - 1)


def act(blob, map) -> bool:
    width = blob.game.width
    height = blob.game.height
    left = map[blob.y][modulo(blob.x - 1, width)]
    right = map[blob.y][modulo(blob.x + 1, width)]
    top = map[modulo(blob.y - 1, height)][blob.x]
    bottom = map[modulo(blob.y + 1, height)][blob.x]
    input_vector = np.array([blob.x, blob.y, left, right, top, bottom, blob.energy, blob.memory])
    result = blob.brain.run(input_vector)

    if not move(blob, result[:4]):
        return False

    if result[4] > BIRTH_THRESHOLD:
        birth(blob)

    eat(blob, map)

    return True


def move(blob, move_decision) -> bool:
    direction_index = move_decision[:4].argmax()
    if direction_index == 0:
        blob.y = modulo(blob.y - 1, blob.game.height)
    elif direction_index == 1:
        blob.y = modulo(blob.y + 1, blob.game.height)
    elif direction_index == 2:
        blob.x = modulo(blob.x - 1, blob.game.width)
    else:
        blob.x = modulo(blob.x + 1, blob.game.width)
    blob.energy -= MOVE_ENERGY_LOSS
    if blob.energy <= 0:
        return False  # blob died from exhaustion
    return True  # blob gets to live another day


def birth(blob):
    from game.models import Blob
    if blob.game.blobs.count() < MAX_BLOB_COUNT:
        Blob.objects.create(
            game=blob.game,
            x=blob.x,
            y=blob.y,
            age=0,
            energy=round(0.5 * blob.energy),
            color=blob.color,
            memory=random(),
            brain=blob.brain
        )
    blob.energy = round(0.5 * blob.energy)


def eat(blob, map):
    if map[blob.y][blob.x] == FOOD_TILE:
        blob.energy = 100
