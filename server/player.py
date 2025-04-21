from fastapi import WebSocket
from uuid import uuid4
import random


def new_module(name, max_cooldown, weapon_id=None):
    angle = random.uniform(-3.5, 3.5)
    m = {
        'module_id': str(uuid4()),
        'name': name,
        'cooldown': 0,
        'max_cooldown': max_cooldown,
        'offset_angle': angle,
        'distance': random.randint(20, 50),
        'aim_angle': angle,
        'colour': random.choice(["red", "green", "yellow"]),
    }
    if weapon_id:
        m['weapon_id'] = weapon_id
    return m


def default_weapons():
    ws = []
    for name, weapon_id, max_cooldown in [
        ("rapido", "rapid", 0.2),
        ("spready", "spread", 0.3),
        ("rapida", "rapid", 0.2),
        ("spreadu", "spread", 0.3),
    ]:
        ws.append(new_module(name, max_cooldown, weapon_id))
    return ws


def default_modules():
    dms = []

    for name, max_cooldown in [
        ("shield", 5),
        ("boost", 5),
        ("quad", 5),
    ]:
        dms.append(new_module(name, max_cooldown))
    return dms + default_weapons()


def default_player(ws: WebSocket):
    return {
        "ws": ws,
        "x": 0,
        "y": 0,
        "vx": 0,
        "vy": 0,
        "a": 0,
        "speed": 5,
        'hp': 10,
        'colour': random.choice(["red", "green", "yellow"]),
        "modules": default_modules()
    }


class MockInventory:
    """
    This is a mock inventory for testing purposes.
    It contains a list of weapons with their properties.
    """

    def __init__(self):
        self.inventory = {}

    def get(self, pid):
        if pid not in self.inventory:
            self.inventory[pid] = self.default_inventory()
        return self.inventory[pid]

    def set(self, pid, inventory):
        self.inventory = inventory

    def default_inventory(self):
        return [new_module('sring', 1, 'spread'),
                new_module('sraing', 0.5, 'rapid'),
                 *default_modules()
                ]


mock_inventory = MockInventory()
