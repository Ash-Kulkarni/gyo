import math
from .modules import activate_modules
from .types import AppState


def compute_total_angle(base: float, offset: float = 0, aim: float = 0) -> float:
    """Combine ship’s facing, bay offset and optional aim‐adjustment."""
    return base + offset + aim


def compute_velocity(
    angle: float, speed: float, player_vx: float = 0, player_vy: float = 0
) -> tuple[float, float]:
    """Return (vx,vy) = unit‐vector(angle) * (speed + move_speed)."""
    # if this weapon uses the ship velocity
    # return math.cos(angle) * speed + player_vx, math.sin(angle) * speed + player_vy

    # or if this is a light based weapon then it should be a constant speed
    return math.cos(angle) * speed, math.sin(angle) * speed


def spawn_point(
    x: float, y: float, angle: float, distance: float
) -> tuple[float, float]:
    """Return world coords of a bay given its angle & distance from ship center."""
    return x + math.cos(angle) * distance, y + math.sin(angle) * distance


def handle_fire_all(player, s, pid):
    x, y = player["x"], player["y"]
    ship_angle = player["a"]
    player_vx = player["vx"]
    player_vy = player["vy"]

    weapons = [m for m in player["modules"] if m.get("weapon_id")]
    for w in weapons:
        if w["cooldown"] > 0:
            continue
        w["cooldown"] = w["max_cooldown"]

        spawn_projectiles(s, w, player_vx, player_vy, pid, ship_angle, x, y)


def spawn_projectiles(s, w, player_vx, player_vy, pid, ship_angle, x, y):
    weapon_id = w["weapon_id"]
    offset = w.get("offset_angle", 0)
    aim = w.get("aim_angle", 0)
    dist = w.get("distance", 20)

    mount_angle = compute_total_angle(ship_angle, offset, 0)
    bx, by = spawn_point(x, y, mount_angle, dist)

    def add_projectile(vx, vy):
        s.bullets.append(
            {
                "x": bx,
                "y": by,
                "vx": vx,
                "vy": vy,
                "from": pid,
                "radius": 2,
            }
        )

    if weapon_id == "rapid":
        # speed = 12
        fire_angle = compute_total_angle(ship_angle, 0, aim)
        vx, vy = compute_velocity(fire_angle, 32, player_vx, player_vy)
        add_projectile(vx, vy)

    elif weapon_id == "spread":
        # speed = 8
        for spread in (-0.2, 0, 0.2):
            fire_angle = compute_total_angle(ship_angle, spread, aim)
            vx, vy = compute_velocity(fire_angle, 28, player_vx, player_vy)
            add_projectile(vx, vy)


def clamp_players_to_world_bounds(s: AppState, dt: float):
    """Clamp players to world bounds."""
    for pid, p in s.players.items():
        clamped_x, clamped_y = clamp_to_world_bounds(s.world_size, p["x"], p["y"])
        p["x"] = clamped_x
        p["y"] = clamped_y


async def handle_client_input(s: AppState, dt: float, input_data, pid, inventory):
    p = s.players[pid]
    mass = 0.6
    accel = 650 / mass
    friction = 25
    max_speed = p.get("speed", 0) * 65
    angle_accel = 8
    max_turn_speed = 1800
    springiness = 2
    damping = 4

    move_x, move_y = None, None
    if input_data.get("move", False):
        move_x = input_data["move"]["x"]
        move_y = input_data["move"]["y"]
        move_angle = math.atan2(move_y, move_x)

        p["vx"] = move_x * accel * dt
        p["vy"] = move_y * accel * dt

        p["vx"] -= friction * p["vx"] * dt
        p["vy"] -= friction * p["vy"] * dt

        speed = math.sqrt(p["vx"] ** 2 + p["vy"] ** 2)
        if speed > max_speed:
            p["vx"] = (p["vx"] / speed) * max_speed
            p["vy"] = (p["vy"] / speed) * max_speed

    desired_angle = None
    if input_data.get("aim", False):
        aim = input_data["aim"]
        desired_angle = math.atan2(aim["y"], aim["x"])
    elif move_x or move_y:
        desired_angle = move_angle
    if desired_angle is not None:
        delta = (desired_angle - p["a"] + math.pi) % (2 * math.pi) - math.pi
        p["angle_velocity"] += delta * springiness * dt * angle_accel
        p["angle_velocity"] -= damping * p["angle_velocity"] * dt
        turn_speed = max_turn_speed * dt

        p["angle_velocity"] = max(-max_turn_speed, min(p["angle_velocity"], turn_speed))
        p["a"] += p["angle_velocity"] * dt

    if input_data.get("activate_modules", False):
        if module_ids := input_data["activate_modules"]:
            await activate_modules(p, module_ids)

    if input_data.get("fire"):
        handle_fire_all(p, s, pid)

    handle_editor_input(input_data, pid, p, inventory)


def clamp_to_world_bounds(world_size, x, y):
    """Clamp coordinates to world bounds."""
    w = world_size.get("width", None)
    h = world_size.get("height", None)
    if w is None or h is None:
        raise ValueError("World size not defined")

    x = max(-w / 2, min(x, w / 2))
    y = max(-h / 2, min(y, h / 2))
    return x, y


def get_module_id(input_data):
    module_id = input_data.get("module_id")
    if module_id is None:
        raise ValueError(f"Module {module_id} not found in equipped modules")

    return module_id


def handle_editor_input(input_data, pid, player, inventory):
    match input_data.get("event"):
        case "equip_module":
            module_id = get_module_id(input_data)
            equipped = {m["module_id"] for m in player["modules"]}
            mod_to_equip = next(
                (
                    m
                    for m in inventory
                    if m["module_id"] == module_id and module_id not in equipped
                ),
                None,
            )
            if mod_to_equip is None:
                raise ValueError(f"Module {module_id} not found in inventory")
            player["modules"].append(mod_to_equip)
        case "unequip_module":
            module_id = get_module_id(input_data)
            player["modules"] = [
                m for m in player["modules"] if m["module_id"] != module_id
            ]
        case "edit_module_position":
            module_id = get_module_id(input_data)
            mod = next(
                (m for m in player["modules"] if m["module_id"] == module_id), None
            )
            if mod is None:
                return
            mod["distance"] = input_data.get("data", {}).get(
                "distance", mod["distance"]
            )
            mod["offset_angle"] = input_data.get("data", {}).get(
                "offset_angle", mod["offset_angle"]
            )
        case "edit_module_aim":
            module_id = get_module_id(input_data)
            mod = next(
                (m for m in player["modules"] if m["module_id"] == module_id), None
            )
            if mod is None:
                return
            mod["aim_angle"] = input_data.get("data", {}).get(
                "aim_angle", mod["aim_angle"]
            )
