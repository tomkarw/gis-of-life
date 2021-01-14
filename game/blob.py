import numpy as np

from game.utils import create_blob


def act(blob, map):
    left = map[blob.x - 1][blob.y]
    right = map[blob.x + 1][blob.y]
    top = map[blob.x][blob.y - 1]
    bottom = map[blob.x][blob.y + 1]
    input_vector = np.array([blob.x, blob.y, left, right, top, bottom, blob.energy, blob.memory])
    result = blob.brain.run(input_vector)

    if not blob.move(result[:4]):
        blob.delete()
        return False

    action_index = result.index(max(result[4:6]))
    if action_index == 4:
        birth(blob)
    else:
        eat(blob)


def move(blob, move_decision):
    direction_index = move_decision.index(max(move_decision[:4]))
    if direction_index == 0:
        blob.y = (blob.y - 1) % blob.game.height
    elif direction_index == 1:
        blob.y = (blob.y + 1) % blob.game.height
    elif direction_index == 2:
        blob.x = (blob.x - 1) % blob.game.width
    else:
        blob.x = (blob.x + 1) % blob.game.width
    blob.energy -= 10
    if blob.energy <= 0:
        return False  # blob died from exhaustion
    return True  # blob gets to live another day


def birth(blob):
    create_blob(blob.game)  # TODO: make them proper descendant
    blob.energy = round(0.5 * blob.energy)


def eat(self):
    self.energy = 100
