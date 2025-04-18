import math


def handle_fire_all(player, angle, move_speed, bullets):

    x, y = player["x"], player["y"]
    projectiles = []

    for bay in player.get("bays", []):
        if bay["cooldown"] > 0:
            continue
        bay["cooldown"] = bay['max_cooldown']

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
                "from": id(player),
                "radius": 2,
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
                    "from": id(player),
                    "radius": 2,
                })

    bullets.extend(projectiles)


def handle_client_input(players, bullets, input_data, pid):

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
        print(f"Firing from {pid}")
        handle_fire_all(players[pid], players[pid]['a'], move_speed, bullets)
