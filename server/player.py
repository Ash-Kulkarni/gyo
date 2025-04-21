from fastapi import WebSocket


def default_weapons():
    return [
        {
            "module_id": 10,
            "weapon_id": "rapid",
            "name": "el rapido",
            "cooldown": 0,
            "max_cooldown": 0.2,
            "offset_angle": 0.2,
            "distance": 20,
            "aim_angle": 0
        },
        {
            "module_id": 11,
            "weapon_id": "rapid",
            "name": "el rapido",
            "cooldown": 0,
            "max_cooldown": 0.2,
            "offset_angle": -0.2,
            "distance": 20,
            "aim_angle": 0
        },

        {
            "module_id": 12,
            "weapon_id": "rapid",
            "name": "el rapido",
            "cooldown": 0,
            "max_cooldown": 0.2,
            "offset_angle": 1,
            "distance": 50,
            "aim_angle": 0
        },
        {
            "module_id": 13,
            "weapon_id": "rapid",
            "name": "el rapido",
            "cooldown": 0,
            "max_cooldown": 0.2,
            "offset_angle": -1,
            "distance": 50,
            "aim_angle": 0
        },

        {
            "module_id": 14,
            "weapon_id": "spread",
            "name": "la buerre",
            "cooldown": 0,
            "max_cooldown": 0.3,
            "offset_angle": 1.5,
            "distance": 30,
            "aim_angle": 0
        },
        {
            "module_id": 15,
            "weapon_id": "spread",
            "name": "la buerre",
            "cooldown": 0,
            "max_cooldown": 0.3,
            "offset_angle": -1.5,
            "distance": 30,
            "aim_angle": 0
        },
    ]


def default_modules():
    return [
        {
            'module_id': 1,
            'name': 'boost',
            'cooldown': 0,
            'max_cooldown': 5,
            "offset_angle": 0.8,
            "distance": 30,
            "aim_angle": 0
        },
        {
            'module_id': 2,
            'name': 'boost',
            'cooldown': 0,
            'max_cooldown': 5,
            "offset_angle": -0.8,
            "distance": 30,
            "aim_angle": 0
        },
        {
            'module_id': 3,
            'name': 'shield',
            'cooldown': 0,
            'max_cooldown': 5,
            "offset_angle": -3.5,
            "distance": 30,
            "aim_angle": 0
        },
        *default_weapons(),

    ]


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
        return [
            {
                "module_id": 10,
                "weapon_id": "rapid",
                "name": "inv weapon 1",
                "cooldown": 0,
                "max_cooldown": 0.2,
                "offset_angle": 0.2,
                "distance": 20,
                "aim_angle": 0
            },
            {
                "module_id": 11,
                "weapon_id": "rapid",
                "name": "inv weapon 2",
                "cooldown": 0,
                "max_cooldown": 0.2,
                "offset_angle": -0.2,
                "distance": 20,
                "aim_angle": 0
            },

            {
                "module_id": 12,
                "weapon_id": "rapid",
                "name": "inv weapon 3",
                "cooldown": 0,
                "max_cooldown": 0.2,
                "offset_angle": 1,
                "distance": 50,
                "aim_angle": 0
            },
            {
                "module_id": 13,
                "weapon_id": "rapid",
                "name": "inv weapon 4",
                "cooldown": 0,
                "max_cooldown": 0.2,
                "offset_angle": -1,
                "distance": 50,
                "aim_angle": 0
            },

            {
                "module_id": 14,
                "weapon_id": "spread",
                "name": "inv weapon 5",
                "cooldown": 0,
                "max_cooldown": 0.3,
                "offset_angle": 1.5,
                "distance": 30,
                "aim_angle": 0
            },
            {
                "module_id": 15,
                "weapon_id": "spread",
                "name": "inv weapon 6",
                "cooldown": 0,
                "max_cooldown": 0.3,
                "offset_angle": -1.5,
                "distance": 30,
                "aim_angle": 0
            },
        ]

mock_inventory = MockInventory()
