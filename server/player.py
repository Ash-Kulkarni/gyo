from fastapi import WebSocket


def default_bay():
    return [
        {"weapon_id": "rapid",
         "cooldown": 0,
         "max_cooldown": 0.2,
         "offset_angle": 2.3,
         "distance": 20
         },
        {"weapon_id": "rapid", "cooldown": 0, "max_cooldown": 0.2,
         "offset_angle": -2.3,
         "distance": 20
         },
        {"weapon_id": "spread", "cooldown": 0, "max_cooldown": 1,
         "offset_angle": 5,
         "distance": 20
         },
        {"weapon_id": "spread", "cooldown": 0, "max_cooldown": 1,
         "offset_angle": -5,
         "distance": 20
         },
        {"weapon_id": "spread", "cooldown": 0, "max_cooldown": 0.2,
         "offset_angle": 8,
         "distance": 45
         },
        {"weapon_id": "spread", "cooldown": 0, "max_cooldown": 0.2,
         "offset_angle": -8,
         "distance": 45
         },
    ]


def default_modules():
    return [
        {
            'module_id': 1,
            'name': 'boost',
            'cooldown': 0,
            'max_cooldown': 5,
        },
        {
            'module_id': 2,
            'name': 'boost',
            'cooldown': 0,
            'max_cooldown': 5,
        },
        {
            'module_id': 3,
            'name': 'shield',
            'cooldown': 0,
            'max_cooldown': 5,
        },

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
        "bays": default_bay(),
        'hp': 10,
        "modules": default_modules()
    }
