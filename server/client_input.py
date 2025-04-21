import math
from .modules import activate_modules


def compute_total_angle(base: float, offset: float = 0, aim: float = 0) -> float:
    """Combine ship’s facing, bay offset and optional aim‐adjustment."""
    return base + offset + aim


def compute_velocity(angle: float, speed: float, move_speed: float) -> tuple[float, float]:
    """Return (vx,vy) = unit‐vector(angle) * (speed + move_speed)."""
    mag = speed + move_speed
    return math.cos(angle) * mag, math.sin(angle) * mag


def spawn_point(x: float, y: float, angle: float, distance: float) -> tuple[float, float]:
    """Return world coords of a bay given its angle & distance from ship center."""
    return x + math.cos(angle) * distance, y + math.sin(angle) * distance


def handle_fire_all(player, bullets, pid):

    x, y = player["x"], player["y"]
    ship_angle = player['a']
    move_speed = player.get("speed", 0)

    weapons = [m for m in player['modules'] if m.get("weapon_id")]
    for w in weapons:
        if w["cooldown"] > 0:
            continue
        w["cooldown"] = w['max_cooldown']

        weapon_id = w["weapon_id"]
        offset = w.get("offset_angle", 0)
        aim = w.get("aim_angle", 0)
        dist = w.get("distance", 20)

        mount_angle = compute_total_angle(ship_angle, offset, 0)
        bx, by = spawn_point(x, y, mount_angle, dist)

        def add_projectile(vx, vy):
            bullets.append({
                "x": bx,
                "y": by,
                "vx": vx,
                "vy": vy,
                "from": pid,
                "radius": 2,
            })

        if weapon_id == "rapid":
            # speed = 12
            fire_angle = compute_total_angle(ship_angle, 0, aim)
            vx, vy = compute_velocity(fire_angle,  12, move_speed)
            add_projectile(vx, vy)

        elif weapon_id == "spread":
            # speed = 8
            for spread in (-0.2, 0, 0.2):
                fire_angle = compute_total_angle(ship_angle, spread, aim)
                vx, vy = compute_velocity(
                    fire_angle, 8, move_speed)
                add_projectile(vx, vy)


async def handle_client_input(players, bullets, input_data, pid, inventory):

    move_x = input_data.get("move", {}).get("x", 0)
    move_y = input_data.get("move", {}).get("y", 0)
    move_angle = math.atan2(move_y, move_x)

    move_speed = players[pid].get("speed", 0)
    players[pid]["x"] += move_x * move_speed
    players[pid]["y"] += move_y * move_speed

    if input_data.get("activate_modules", False):
        if module_ids := input_data["activate_modules"]:
            await activate_modules(players[pid], module_ids)

    if input_data.get("aim", False):
        # print(input_data)
        aim_x = input_data.get("aim", {}).get("x", 0)
        aim_y = input_data.get("aim", {}).get("y", 0)
        angle = math.atan2(aim_y, aim_x)
        players[pid]['a'] = angle
    elif (move_x or move_y):
        players[pid]['a'] = move_angle

    players[pid]["x"] = max(-2000, min(players[pid]["x"], 2000))
    players[pid]["y"] = max(-2000, min(players[pid]["y"], 2000))
    if input_data.get("fire"):
        handle_fire_all(players[pid],
                        bullets, pid)
    # print(input_data)
    handle_editor_input(
        input_data, pid, players[pid], inventory
    )


def get_module_id(input_data):

    module_id = input_data.get("module_id")
    if module_id is None:
        raise ValueError(
            f'Module {module_id} not found in equipped modules')

    return module_id


def handle_editor_input(
    input_data, pid, player, inventory

):
    match input_data.get("event"):
        case "equip_module":
            module_id = get_module_id(input_data)
            unequipped = {m['module_id'] for m in inventory} - \
                {m["module_id"] for m in player["modules"]}
            mod_to_equip = next(
                (m for m in inventory if m["module_id"] == module_id), None)
            if mod_to_equip is None:
                raise ValueError(f'Module {module_id} not found in inventory')
            player["modules"].append(mod_to_equip)
        case "unequip_module":
            module_id = get_module_id(input_data)
            player["modules"] = [
                m for m in player["modules"] if m["module_id"] != module_id]
        case "edit_module_position":
            module_id = get_module_id(input_data)
            mod = next(
                (m for m in player["modules"] if m["module_id"] == module_id), None)
            if mod is None:
                return
            mod['distance'] = input_data.get(
                "data", {}).get("distance", mod['distance'])
            mod['offset_angle'] = input_data.get("data", {}).get(
                "offset_angle", mod['offset_angle'])
        case "edit_module_aim":
            module_id = get_module_id(input_data)
            mod = next(
                (m for m in player["modules"] if m["module_id"] == module_id), None)
            if mod is None:
                return
            mod['aim_angle'] = input_data.get(
                "data", {}).get("aim_angle", mod['aim_angle'])
