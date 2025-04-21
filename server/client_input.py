import math
from .modules import activate_modules


def handle_fire_all(player, angle, move_speed, bullets, pid):

    x, y = player["x"], player["y"]
    projectiles = []

    weapons = [m for m in player['modules'] if m.get("weapon_id")]
    for w in weapons:
        if w["cooldown"] > 0:
            continue
        w["cooldown"] = w['max_cooldown']

        weapon_id = w["weapon_id"]
        offset_angle = w.get("offset_angle", 0)
        distance = w.get("distance", 20)

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
                "from": pid,
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
                    "from": pid,
                    "radius": 2,
                })

    bullets.extend(projectiles)


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
        print(input_data)
        aim_x = input_data.get("aim", {}).get("x", 0)
        aim_y = input_data.get("aim", {}).get("y", 0)
        angle = math.atan2(aim_y, aim_x)
        players[pid]['a'] = angle
    elif (move_x or move_y):
        players[pid]['a'] = move_angle

    players[pid]["x"] = max(-2000, min(players[pid]["x"], 2000))
    players[pid]["y"] = max(-2000, min(players[pid]["y"], 2000))
    if input_data.get("fire"):
        handle_fire_all(players[pid], players[pid]
                        ['a'], move_speed, bullets, pid)
    print(input_data)
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
            # equipped_index = input_data.get("equipped_index")
            # position = input_data.get("position")
            # editModulePosition(player["modules"], equipped_index, position)
        case "edit_module_aim":
            module_id = get_module_id(input_data)
            # equipped_index = input_data.get("equipped_index")
            # aim = input_data.get("aim")
            # editModuleAim(player["modules"], equipped_index, aim)

            # const equipModuleFromInventory = (
            #   equippedModules,
            #   inventory,
            #   inventoryIndex,
            # ) => {
            #   console.log("equipModuleFromInventory");
            #   // const item = inventory[inventoryIndex];
            #   // if (!item) return;
            #   // equippedModules.push(item);
            #   // equippedModules.push({...item})
            #   sendInput({
            #     event: "equip_module",
            #     module_id: inventory[inventoryIndex].module_id,
            #   });
            # };
            # const unequipModule = (equippedModules, inventory, equippedIndex) => {
            #   sendInput({
            #     event: "unequip_module",
            #     module_id: equippedModules[equippedIndex].module_id,
            #   });
            #   console.log("unequipModule");
            # };
            # const editModulePosition = (equippedModules, equippedIndex, position) => {
            #   sendInput({
            #     event: "edit_module_position",
            #     module_id: equippedModules[equippedIndex].module_id,
            #     position,
            #   });
            #   console.log("editModulePosition");
            # };
            # const editModuleAim = (equippedModules, equippedIndex, aim) => {
            #   sendInput({
            #     event: "edit_module_aim",
            #     module_id: equippedModules[equippedIndex].module_id,
            #     aim,
            #   });
            #   console.log("editModuleAim");
            # };
