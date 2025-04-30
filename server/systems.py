import math
import random
import json
from .types import AppState


def update_enemy_behavior(s: AppState, dt: float):
    for enemy in s.enemies:
        if enemy["type"] == "chaser":
            # find closest player
            closest = None
            closest_dist = float("inf")
            for p in s.players.values():
                dx = p["x"] - enemy["x"]
                dy = p["y"] - enemy["y"]
                d2 = dx * dx + dy * dy
                if d2 < closest_dist:
                    closest = p
                    closest_dist = d2
                    move_dx = dx
                    move_dy = dy

            if closest:
                dist = math.sqrt(closest_dist)
                if dist > 0:
                    nx = move_dx / dist
                    ny = move_dy / dist
                    speed = enemy.get("speed", 1.5)
                    enemy["x"] += nx * speed * dt
                    enemy["y"] += ny * speed * dt


def respawn_dead_players(s: AppState, dt: float):
    for pid, player in s.players.items():
        if player["hp"] <= 0:
            print(f"💀 Respawning player {pid}")
            player["x"], player["y"] = (
                random.randint(-2000, 2000),
                random.randint(-2000, 2000),
            )
            player["hp"] = 10


async def broadcast_state(s: AppState, dt: float):
    state = read_state(s, dt)

    player_snapshot = list(s.players.values())
    for p in player_snapshot:
        try:
            await p["ws"].send_text(json.dumps(state))
        except:
            continue


def read_state(s: AppState, dt: float):
    return {
        "players": {
            pid: {
                "x": p["x"],
                "y": p["y"],
                "a": p["a"],
                "hp": p["hp"],
                "colour": p["colour"],
                "modules": p["modules"],
            }
            for pid, p in s.players.items()
        },
        "bullets": s.bullets,
        "enemies": s.enemies,
        "scoreboard": {
            pid: {"kills": p["kills"]}
            for pid, p in s.players.items()
            if p.get("kills") is not None
        },
    }


def remove_out_of_bounds_bullets(s: AppState, dt: float):
    s.bullets[:] = [
        b for b in s.bullets if -2000 < b["x"] < 2000 and -2000 < b["y"] < 2000
    ]


def tick_player_weapon_cooldowns(s: AppState, dt: float):
    for p in s.players.values():
        weapons = [m for m in p["modules"] if m.get("weapon_id")]
        for weapon in weapons:
            weapon["cooldown"] = max(0, weapon["cooldown"] - dt)


def tick_bullets_velocity(s: AppState, dt: float):
    for b in s.bullets:
        b["x"] += b["vx"] * dt
        b["y"] += b["vy"] * dt


def tick_player_velocity(s: AppState, dt: float):
    w = s.world_size.get("width", None)
    h = s.world_size.get("height", None)
    if w is None or h is None:
        raise ValueError("World size not defined")
    for p in s.players.values():
        p["x"] += p["vx"] * dt
        p["y"] += p["vy"] * dt
        p["x"] = max(-w / 2, min(p["x"], w / 2))
        p["y"] = max(-h / 2, min(p["y"], h / 2))


def tick_enemy_velocity(s: AppState, dt: float):
    for e in s.enemies:
        e["x"] += e["vx"] * dt
        e["y"] += e["vy"] * dt
