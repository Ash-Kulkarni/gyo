import math
from enum import Enum



class Shape(Enum):
    # CIRCLE = "circle"
    SQUARE = "square"
    TRIANGLE = "triangle"
    HEXAGON = "hexagon"


def regular_polygon(sides, radius):
    return [
        (
            radius * math.cos(2 * math.pi * i / sides),
            radius * math.sin(2 * math.pi * i / sides)
        )
        for i in range(sides)
    ]

SHAPES = {
    "triangle": [(-10, 10), (10, 10), (0, -10)],
    "square": [(-10, -10), (10, -10), (10, 10), (-10, 10)],
    "hexagon": regular_polygon(6, 10),
}
