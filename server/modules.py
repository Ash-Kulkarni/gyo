import asyncio
from .types import AppState


async def activate_module(player, module_id):
    module = next((m for m in player["modules"] if m["module_id"] == module_id), None)
    if module is None:
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
