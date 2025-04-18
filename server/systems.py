import math
import random
import json


def update_enemy_behavior(enemies, players):
    for enemy in enemies:
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


def handle_enemy_player_collisions(players, enemies):
    for pid, player in players.items():
        px, py = player["x"], player["y"]
        for enemy in enemies:
            dx = enemy["x"] - px
            dy = enemy["y"] - py
            dist_sq = dx * dx + dy * dy
            if dist_sq < (20 ** 2):  # collision range
                player["hp"] -= 1  # basic contact damage


def respawn_dead_players(players):

    for pid, player in players.items():

        if player["hp"] <= 0:

            print(f"💀 Respawning player {pid}")

            player["x"], player["y"] = random.randint(-2000, 2000), random.randint(-2000, 2000)

            player["hp"] = 10

async def broadcast_state(players, state):

    for p in players.values():
        try:
            await p["ws"].send_text(json.dumps(state))
        except:
            continue


def read_state(players, bullets, enemies):

    state = {

        "players": {

            pid: {"x": p["x"], "y": p["y"], "a": p["a"], "bays": p["bays"], 'hp': p['hp']} for pid, p in players.items()

        },

        'bullets': bullets,

        'enemies': enemies,

    }

    return state
def remove_out_of_bounds_bullets(bullets):

    bullets[:] = [b for b in bullets if -2000 < b['x'] < 2000 and -2000 < b['y'] < 2000]

def tick_player_weapon_cooldowns(players, TICK_RATE):
    for p in players.values():
        for weapon in p["bays"]:
            weapon["cooldown"] = max(0, weapon["cooldown"] - TICK_RATE)

def tick_bullets_velocity(bullets):
    for b in bullets:
        b["x"] += b["vx"]
        b["y"] += b["vy"]

