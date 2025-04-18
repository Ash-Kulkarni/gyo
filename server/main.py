from fastapi.websockets import WebSocketDisconnect
from fastapi import FastAPI, WebSocket
import math
import random
import json
import asyncio
import os
from enum import Enum

def is_testing():
    return os.getenv("TESTING", "0") == "1"


app = FastAPI()
players = {}
bullets = []

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


enemies = [spawn_enemy(102, 102)]


def maybe_spawn_enemies(enemies):
    if len(enemies) < 10:
        x = random.randint(-2000, 2000)
        y = random.randint(-2000, 2000)
        enemies.append(spawn_enemy(x, y))


def dist_sq(x1, y1, x2, y2):
    return (x1 - x2)**2 + (y1 - y2)**2


def check_bullet_collisions(bullets, enemies):
    hit_radius_sq = 16  # ~4 px hit radius

    dead_enemies = []
    live_bullets = []

    for bullet in bullets:
        hit = False
        for enemy in enemies:
            if dist_sq(bullet["x"], bullet["y"], enemy["x"], enemy["y"]) < hit_radius_sq:
                enemy["hp"] -= 1  # simple damage
                hit = True
                break
        if not hit:
            live_bullets.append(bullet)

    # Cull dead enemies
    for e in enemies:
        if e["hp"] <= 0:
            dead_enemies.append(e)
    enemies[:] = [e for e in enemies if e["hp"] > 0]

    return live_bullets, dead_enemies


def default_bay():
    return [
        {"weapon_id": "rapid", "cooldown": 0,
         "offset_angle": 2.3,
         "distance": 20
         },
        {"weapon_id": "rapid", "cooldown": 0,
         "offset_angle": -2.3,
         "distance": 20
         },
        # {"weapon_id": "spread", "cooldown": 0,
        #  "offset_angle": 5,
        #  "distance": 20
        #  },
        # {"weapon_id": "spread", "cooldown": 0,
        #  "offset_angle": -5,
        #  "distance": 20
        #  },
    ]


def default_player(ws: WebSocket):
    return {"ws": ws, "x": 0, "y": 0, "vx": 0, "vy": 0, "a": 0, "bays": default_bay(), 'hp': 10}


def handle_fire_all(player, angle, move_speed):

    x, y = player["x"], player["y"]
    projectiles = []

    for bay in player.get("bays", []):
        if bay["cooldown"] > 0:
            continue
        bay["cooldown"] = 0.2

        weapon_id = bay["weapon_id"]
        offset_angle = bay.get("offset_angle", 0)
        distance = bay.get("distance", 20)

        spawn_angle = angle + offset_angle
        bx = x + math.cos(spawn_angle) * distance
        by = y + math.sin(spawn_angle) * distance

        if weapon_id == "rapid":
            speed = 12
            total_speed = speed + move_speed
            projectiles.append({
                "x": bx, "y": by,
                "vx": math.cos(angle) * total_speed,
                "vy": math.sin(angle) * total_speed,
                "from": id(player)
            })

        elif weapon_id == "spread":
            speed = 8
            total_speed = speed + move_speed
            for spread in [-0.2, 0.0, 0.2]:
                sx = math.cos(angle + spread) * total_speed
                sy = math.sin(angle + spread) * total_speed
                projectiles.append({
                    "x": bx, "y": by,
                    "vx": sx, "vy": sy,
                    "from": id(player)
                })

    bullets.extend(projectiles)


@app.websocket("/ws")
async def ws_endpoint(ws: WebSocket):

    pid = str(id(ws))
    await ws.accept()
    await ws.send_text(json.dumps({"type": "hello", "pid": pid}))
    print(f"🔌 Player connected: {pid}")
    players[pid] = default_player(ws)

    try:
        while True:
            data = await ws.receive_text()
            input_data = json.loads(data)
            if not input_data:
                continue

            move_x = input_data.get("move", {}).get("x", 0)
            move_y = input_data.get("move", {}).get("y", 0)
            move_angle = math.atan2(move_y, move_x)

            move_speed = 5
            players[pid]["x"] += move_x * move_speed
            players[pid]["y"] += move_y * move_speed

            if input_data.get("dash", False) and (move_x or move_y):
                dash_strength = 10
                players[pid]['x'] += math.cos(move_angle) * dash_strength
                players[pid]['y'] += math.sin(move_angle) * dash_strength

            if input_data.get("aim", False):
                aim_x = input_data.get("aim", {}).get("x", 0)
                aim_y = input_data.get("aim", {}).get("y", 0)
                angle = math.atan2(aim_y, aim_x)
                players[pid]['a'] = angle
            elif (move_x or move_y):
                players[pid]['a'] = move_angle

            players[pid]["x"] = max(-2000, min(players[pid]["x"], 2000))
            players[pid]["y"] = max(-2000, min(players[pid]["y"], 2000))
            if input_data.get("fire"):
                handle_fire_all(
                    players[pid], players[pid]['a'], move_speed)

            # 🚨 Send response immediately if testing
            if is_testing():
                await broadcast_loop()

    except WebSocketDisconnect:
        print(f"❌ Player disconnected: {pid}")
        del players[pid]


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


def handle_enemy_player_collisions():
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

async def broadcast_loop():
    FRAME_RATE = 60
    TICK_RATE = 1 / FRAME_RATE
    global players, bullets, enemies
    while True:
        state = read_state(players, bullets, enemies)
        print(f"Broadcasting state: {state}")

        tick_player_weapon_cooldowns(players, TICK_RATE)
        update_enemy_behavior(enemies, players)
        maybe_spawn_enemies(enemies)
        handle_enemy_player_collisions()
        respawn_dead_players(players)
        await broadcast_state(players, state)
        await asyncio.sleep(TICK_RATE)
        tick_bullets_velocity(bullets)
        [next_bullets, _dead_enemies] = check_bullet_collisions(bullets, enemies)
        bullets = next_bullets
        remove_out_of_bounds_bullets(bullets)



@app.on_event("startup")
async def startup_event():
    print("🚀 Server starting...")
    asyncio.create_task(broadcast_loop())
