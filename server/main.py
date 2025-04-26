from fastapi.websockets import WebSocketDisconnect
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import json
import asyncio
import os

from .player import default_player, mock_inventory
from .systems import (
    tick_bullets_velocity,
    tick_player_velocity,
    tick_enemy_velocity,
    update_enemy_behavior,
    respawn_dead_players,
    remove_out_of_bounds_bullets,
    broadcast_state,
    tick_player_weapon_cooldowns,
)
from .enemies import maybe_spawn_enemies
from .collision import check_bullet_collisions, handle_enemy_player_collisions
from .modules import tick_modules
from .types import AppState
from .client_input import handle_client_input


def is_testing():
    return os.getenv("TESTING", "0") == "1"


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/inventory/{pid}", status_code=200)
async def get_inventory(pid: str):
    inventory = mock_inventory.get(pid)
    if not inventory:
        print(f"Inventory not found for player {pid}")
        return {"error": "Inventory not found"}
    print(f"Inventory for player {pid}: {inventory}")
    return inventory


@app.websocket("/ws")
async def ws_endpoint(ws: WebSocket):
    pid = str(id(ws))
    await ws.accept()
    await ws.send_text(json.dumps({"type": "hello", "pid": pid}))
    print(f"🔌 Player connected: {pid}")
    players = app.state.players
    bullets = app.state.bullets
    scoreboard = app.state.scoreboard
    players[pid] = default_player(ws)
    scoreboard[pid] = {"kills": 0}

    try:
        while True:
            data = await ws.receive_text()
            input_data = json.loads(data)
            if not input_data:
                continue
            current_time = asyncio.get_event_loop().time()
            last_input_time = players[pid].get(
                "last_input_time") or current_time
            print("current_time", current_time)
            print("last_input_time", last_input_time)
            dt = current_time - last_input_time
            players[pid]["last_input_time"] = current_time
            await handle_client_input(
                app.state, dt, input_data, pid, inventory=mock_inventory.get(
                    pid)
            )

            if is_testing():
                await broadcast_loop(app.state)

    except WebSocketDisconnect:
        print(f"❌ Player disconnected: {pid}")
        del players[pid]


all_systems = [
    tick_player_weapon_cooldowns,
    update_enemy_behavior,
    maybe_spawn_enemies,
    handle_enemy_player_collisions,
    respawn_dead_players,
    tick_bullets_velocity,
    tick_player_velocity,
    tick_enemy_velocity,
    check_bullet_collisions,
    remove_out_of_bounds_bullets,
    tick_modules,
]


def run_systems(s: AppState, dt: float):
    for func in all_systems:
        func(s, dt)


async def broadcast_loop(s: AppState):
    last_time = asyncio.get_event_loop().time()
    while True:
        current_time = asyncio.get_event_loop().time()
        dt = (current_time - last_time) * 30
        last_time = current_time
        run_systems(s, dt)
        await broadcast_state(s, dt)
        await asyncio.sleep(0)


@app.on_event("startup")
async def startup_event():
    print("🚀 Server starting...")
    app.state.players = {}
    app.state.bullets = []
    app.state.enemies = []
    app.state.scoreboard = {}
    app.state.world_size = {
        "width": 4000,
        "height": 4000,
    }
    asyncio.create_task(broadcast_loop(app.state))
