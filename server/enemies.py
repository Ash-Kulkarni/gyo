import random
from enum import Enum

class Shape(Enum):
    CIRCLE = "circle"
    SQUARE = "square"
    TRIANGLE = "triangle"
    HEXAGON = "hexagon"


def spawn_enemy(x, y, type="chaser"):
    return {
        "x": x,
        "y": y,
        "vx": 0,
        "vy": 0,
        "hp": 1,
        "type": type,
        "speed": 1.5,
        "radius": 10,  # for hit detection
        "shape_id":  random.choice(list(Shape)).value
    }




def maybe_spawn_enemies(enemies):
    if len(enemies) < 10:
        x = random.randint(-2000, 2000)
        y = random.randint(-2000, 2000)
        enemies.append(spawn_enemy(x, y))


