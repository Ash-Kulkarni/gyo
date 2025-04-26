import random
from enum import Enum
from .shared.shapes import Shape
from .types import AppState


class EnemyType(Enum):
    CHASER = "chaser"


ENEMY_COLOURS = ["#ff4b4b", "#ff944b", "#ffe14b", "#4bff75", "#4bd5ff", "#9b4bff"]


def spawn_enemy(x, y, type=EnemyType.CHASER.value):
    return {
        "x": x,
        "y": y,
        "vx": 0,
        "vy": 0,
        "hp": 1,
        "type": type,
        "speed": random.uniform(1, 4),
        "radius": 10,  # for hit detection
        "shape_id": random.choice(list(Shape)).value,
        "colour": random.choice(ENEMY_COLOURS),
    }


def maybe_spawn_enemies(s: AppState):
    if len(s.enemies) < 10:
        x = random.randint(-2000, 2000)
        y = random.randint(-2000, 2000)
        s.enemies.append(spawn_enemy(x, y))
