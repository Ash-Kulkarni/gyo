import math
import random
import json


def update_enemy_behavior(enemies, players):
    for enemy in enemies:
        if enemy["type"] == "chaser":
            # find closest player
            closest = None
            closest_dist = float("inf")
            for p in players.values():
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
                    enemy["x"] += nx * speed
                    enemy["y"] += ny * speed


def respawn_dead_players(players):

    for pid, player in players.items():

        if player["hp"] <= 0:

            print(f"💀 Respawning player {pid}")

            player["x"], player["y"] = random.randint(
                -2000, 2000), random.randint(-2000, 2000)

            player["hp"] = 10


async def broadcast_state(players, state):

    for p in players.values():
        try:
            await p["ws"].send_text(json.dumps(state))
        except:
            continue


def read_state(players, bullets, enemies):

    return {
        "players": {
            pid: {"x": p["x"], "y": p["y"], "a": p["a"], "bays": p["bays"], 'hp': p['hp']} for pid, p in players.items()
        },
        'bullets': bullets,
        'enemies': enemies,
        'scoreboard': {pid: {"kills": p["kills"]} for pid, p in players.items() if p.get("kills") is not None},
    }


def remove_out_of_bounds_bullets(bullets):
    bullets[:] = [b for b in bullets if -2000 <
                  b['x'] < 2000 and -2000 < b['y'] < 2000]


def tick_player_weapon_cooldowns(players, TICK_RATE):
    for p in players.values():
        for weapon in p["bays"]:
            weapon["cooldown"] = max(0, weapon["cooldown"] - TICK_RATE)


def tick_bullets_velocity(bullets):
    for b in bullets:
        b["x"] += b["vx"]
        b["y"] += b["vy"]
