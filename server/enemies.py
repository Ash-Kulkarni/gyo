import random
from enum import Enum
from .shared.shapes import Shape
from .types import AppState
import math
import random


def create_projectile(enemy_id, x, y, target_x, target_y, speed=5, colour="red"):
    """Create a projectile aimed at a target."""
    dx, dy = target_x - x, target_y - y
    dist = max(1, (dx**2 + dy**2) ** 0.5)
    return {
        "x": x,
        "y": y,
        "vx": (dx / dist) * speed,
        "vy": (dy / dist) * speed,
        "radius": 3,
        "colour": colour,
        "from": enemy_id,
    }


class EnemyType(Enum):
    CHASER = "chaser"


ENEMY_COLOURS = ["#ff4b4b", "#ff944b",
                 "#ffe14b", "#4bff75", "#4bd5ff", "#9b4bff"]

MOVEMENT_PATTERNS = ["chase", "zigzag", "circle"]


def spawn_enemy(x, y, type=EnemyType.CHASER.value):
    return {
        "id": random.randint(0, 1000000),
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
        "movement_pattern": random.choice(MOVEMENT_PATTERNS),
        "attack_cooldown": 0,
    }


last_enemy_spawn_time = 0


def maybe_spawn_enemies(s: AppState, dt: float):
    global last_enemy_spawn_time
    if len(s.enemies) >= 10:
        return
    if last_enemy_spawn_time > 0:
        last_enemy_spawn_time -= dt

    if last_enemy_spawn_time <= 0:
        last_enemy_spawn_time = random.uniform(0.5, 2.0)
        x = random.randint(-2000, 2000)
        y = random.randint(-2000, 2000)
        s.enemies.append(spawn_enemy(x, y))


def find_closest_player(enemy, players):
    closest = None
    closest_dist = float("inf")
    for p in players.values():
        dx = p["x"] - enemy["x"]
        dy = p["y"] - enemy["y"]
        d2 = dx * dx + dy * dy
        if d2 < closest_dist:
            closest = p
            closest_dist = d2
    return closest, closest_dist


def update_enemy(enemy, players, dt):
    target, _dist = find_closest_player(enemy, players)
    if not target:
        return []

    if enemy["movement_pattern"] == "chase":
        dx, dy = target["x"] - enemy["x"], target["y"] - enemy["y"]
        dist = max(1, (dx**2 + dy**2) ** 0.5)
        enemy["vx"], enemy["vy"] = (
            (dx / dist) * enemy["speed"],
            (dy / dist) * enemy["speed"],
        )
    elif enemy["movement_pattern"] == "zigzag":
        enemy["vx"] = enemy["speed"] * (1 if random.random() > 0.5 else -1)
        enemy["vy"] = enemy["speed"]
    elif enemy["movement_pattern"] == "circle":
        angle = random.uniform(0, 2 * math.pi)
        enemy["vx"] = enemy["speed"] * math.cos(angle)
        enemy["vy"] = enemy["speed"] * math.sin(angle)

    enemy["x"] += enemy["vx"] * dt
    enemy["y"] += enemy["vy"] * dt

    new_projectiles = []
    if enemy["attack_cooldown"] <= 0:
        new_projectiles.append(
            create_projectile(
                enemy["id"],
                enemy["x"],
                enemy["y"],
                target["x"],
                target["y"],
                speed=15,
                colour=enemy["colour"],
            )
        )

        enemy["attack_cooldown"] = random.uniform(3, 8)
    else:
        enemy["attack_cooldown"] -= dt
    return new_projectiles


def tick_enemies(s: AppState, dt: float):
    maybe_spawn_enemies(s, dt)
    _ps = []
    for enemy in s.enemies:
        _ps.extend(update_enemy(enemy, s.players, dt))
    print(f"New projectiles: {_ps}")
    s.bullets[:] = s.bullets + _ps
