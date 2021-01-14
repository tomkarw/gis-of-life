import numpy as np

from game.utils import create_blob


def modulo(val, range):
    return val % (range - 1)


def act(blob, map):
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

    action_index = result[4:6].argmax()
    if action_index == 0:
        birth(blob)
    else:
        eat(blob)


def move(blob, move_decision):
    direction_index = move_decision[:4].argmax()
    if direction_index == 0:
        blob.y = modulo(blob.y - 1, blob.game.height)
    elif direction_index == 1:
        blob.y = modulo(blob.y + 1, blob.game.height)
    elif direction_index == 2:
        blob.x = modulo(blob.x - 1, blob.game.width)
    else:
        blob.x = modulo(blob.x + 1, blob.game.width)
    blob.energy -= 1
    if blob.energy <= 0:
        return False  # blob died from exhaustion
    return True  # blob gets to live another day


def birth(blob):
    create_blob(blob.game)  # TODO: make them proper descendant
    blob.energy = round(0.5 * blob.energy)


def eat(self):
    self.energy = 100
