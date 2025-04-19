from fastapi.websockets import WebSocketDisconnect
from fastapi import FastAPI, WebSocket
import json
import asyncio
import os

from .player import default_player
from .client_input import handle_client_input
from .systems import (
    read_state,
    tick_bullets_velocity,
    update_enemy_behavior,
    respawn_dead_players,
    remove_out_of_bounds_bullets,
    broadcast_state,
    tick_player_weapon_cooldowns
)
from .enemies import maybe_spawn_enemies
from .collision import check_bullet_collisions, handle_enemy_player_collisions
from .modules import tick_modules


def is_testing():
    return os.getenv("TESTING", "0") == "1"


app = FastAPI()


@app.websocket("/ws")
async def ws_endpoint(ws: WebSocket):

    pid = str(id(ws))
    await ws.accept()
    await ws.send_text(json.dumps({"type": "hello", "pid": pid}))
    print(f"🔌 Player connected: {pid}")
    players = app.state.players
    bullets = app.state.bullets
    enemies = app.state.enemies
    scoreboard = app.state.scoreboard
    players[pid] = default_player(ws)
    scoreboard[pid] = {"kills": 0}

    try:
        while True:
            data = await ws.receive_text()
            input_data = json.loads(data)
            if not input_data:
                continue
            await handle_client_input(players, bullets, input_data, pid)

            if is_testing():
                await broadcast_loop(players, bullets, enemies, scoreboard)

    except WebSocketDisconnect:
        print(f"❌ Player disconnected: {pid}")
        del players[pid]


async def broadcast_loop(players, bullets, enemies, scoreboard):
    FRAME_RATE = 60
    TICK_RATE = 1 / FRAME_RATE
    while True:
        state = read_state(players, bullets, enemies)
        print(f"📡 Scoreboard: {scoreboard}")

        tick_player_weapon_cooldowns(players, TICK_RATE)
        update_enemy_behavior(enemies, players)
        maybe_spawn_enemies(enemies)
        handle_enemy_player_collisions(players, enemies)
        respawn_dead_players(players)
        await broadcast_state(players, state)
        await asyncio.sleep(TICK_RATE)
        tick_bullets_velocity(bullets)
        [next_bullets, _dead_enemies] = check_bullet_collisions(
            bullets, enemies, scoreboard)
        bullets[:] = next_bullets
        remove_out_of_bounds_bullets(bullets)
        tick_modules(players, TICK_RATE)


@ app.on_event("startup")
async def startup_event():
    print("🚀 Server starting...")
    app.state.players = {}
    app.state.bullets = []
    app.state.enemies = []
    app.state.scoreboard = {}
    asyncio.create_task(
        broadcast_loop(app.state.players, app.state.bullets, app.state.enemies, app.state.scoreboard)
    )
