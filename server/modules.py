import asyncio
from .types import AppState


async def activate_shield(player):
    player["shielded"] = True
    await asyncio.sleep(2)
    player["shielded"] = False


async def activate_boost(player):
    player["speed"] *= 2
    await asyncio.sleep(5)
    player["speed"] /= 2


QUAD_WEAPONS = [
    {
        "weapon_id": "spread",
        "cooldown": 0,
        "max_cooldown": 0.5,
        "offset_angle": 5,
        "distance": 20,
    },
    {
        "weapon_id": "spread",
        "cooldown": 0,
        "max_cooldown": 0.5,
        "offset_angle": -5,
        "distance": 20,
    },
    {
        "weapon_id": "spread",
        "cooldown": 0,
        "max_cooldown": 0.1,
        "offset_angle": 4,
        "distance": 45,
    },
    {
        "weapon_id": "spread",
        "cooldown": 0,
        "max_cooldown": 0.1,
        "offset_angle": -4,
        "distance": 45,
    },
    {
        "weapon_id": "spread",
        "cooldown": 0,
        "max_cooldown": 0.5,
        "offset_angle": 2,
        "distance": 20,
    },
    {
        "weapon_id": "spread",
        "cooldown": 0,
        "max_cooldown": 0.5,
        "offset_angle": -2,
        "distance": 20,
    },
    {
        "weapon_id": "spread",
        "cooldown": 0,
        "max_cooldown": 0.1,
        "offset_angle": 1,
        "distance": 45,
    },
    {
        "weapon_id": "spread",
        "cooldown": 0,
        "max_cooldown": 0.1,
        "offset_angle": -1,
        "distance": 45,
    },
]


async def activate_quad(player):
    ...
    # original_mods = player["modules"]
    # player["modules"] = QUAD_WEAPONS
    # await asyncio.sleep(5)
    # player["modules"] = original_mods


SHIELD_MODULE = {
    "cooldown": 0.0,
    "max_cooldown": 5.0,
    "name": "shield",
    "effect": lambda player: activate_shield(player),
}

BOOST_MODULE = {
    "cooldown": 0,
    "max_cooldown": 5.0,
    "name": "boost",
    "effect": lambda player: activate_boost(player),
}

QUAD_MODULE = {
    "cooldown": 0,
    "max_cooldown": 5.0,
    "name": "quad",
    "effect": lambda player: activate_quad(player),
}

MODULES = {
    1: SHIELD_MODULE,
    2: QUAD_MODULE,
    3: BOOST_MODULE,
}


async def activate_module(player, module_id):
    module = next((m for m in player["modules"] if m["module_id"] == module_id), None)
    if not module:
        return
    if module["cooldown"] > 0:
        return
    print(f"Activating module {module_id} for player {id(player)}")
    print(module)
    asyncio.create_task(module["effect"](player))
    module["cooldown"] = module["max_cooldown"]


async def activate_modules(player, module_ids):
    await asyncio.gather(
        *(activate_module(player, module_id) for module_id in module_ids)
    )


def tick_modules(s: AppState, dt):
    for p in s.players.values():
        for module in p["modules"]:
            if module["cooldown"] > 0:
                module["cooldown"] -= dt
                module["cooldown"] = max(0, module["cooldown"])
