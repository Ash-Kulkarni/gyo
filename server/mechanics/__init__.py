from dataclasses import dataclass
from typing import Union, List, Any
from enum import Enum


@dataclass
class Polygon:
    points: List[tuple[float, float]]


@dataclass
class Sector:
    x: float
    y: float
    radius: float
    direction: float  # direction of center of the sector in radians
    angle: float  # total spread angle in radians


@dataclass
class Circle:
    x: float
    y: float
    radius: float


@dataclass
class Rectangle:
    x: float
    y: float
    width: float  # we apply half width to the left and half to the right
    height: float  # we apply half height to the top and half to the bottom
    angle: float = 0.0  # rotation angle in radians, default is 0 (no rotation)


class Op(Enum):
    UNION = "union"
    INTERSECTION = "intersection"
    DIFFERENCE = "difference"


@dataclass
class Composite:
    op: Op
    shapes: List["MechanicShape"]


MechanicShape = Union[Circle, Rectangle, Polygon, Sector, Composite]


@dataclass
class MechanicTimer:
    start_telegraph: int
    end_telegraph: int
    resolve: int


@dataclass
class MechanicGroundTelegraph:
    shape: MechanicShape
    timer: MechanicTimer


@dataclass
class MechanicEffect:
    damage: int
    effects: List[Any]


@dataclass
class Mechanic:
    shape: MechanicShape
    timer: MechanicTimer
    effect: MechanicEffect


def get_players_in_shape(shape: MechanicShape) -> List[Any]:
    return []


def apply_effects_to_targets(effects: List[Any], targets: List[Any]):
    for target in targets:
        for effect in effects:
            pass


def apply_damage_to_targets(damage: int, targets: List[Any]):
    for target in targets:
        pass


def resolve_ground_mechanic(mechanic: Mechanic):
    targets = get_players_in_shape(mechanic.shape)
    apply_effects_to_targets(mechanic.effect.effects, targets)
    apply_damage_to_targets(mechanic.effect.damage, targets)


def plus_shape_bomb() -> List[Mechanic]:
    timer = MechanicTimer(start_telegraph=0, end_telegraph=5, resolve=10)
    start = {"x": 0, "y": 0}
    effect = MechanicEffect(damage=100, effects=[])
    return [
        Mechanic(shape=Circle(**start, radius=10), timer=timer, effect=effect),
        Mechanic(
            shape=Rectangle(**start, width=10, height=50), timer=timer, effect=effect
        ),
        Mechanic(
            shape=Rectangle(**start, width=50, height=10), timer=timer, effect=effect
        ),
    ]


def telegraph_mechanic(m: Mechanic) -> MechanicGroundTelegraph:
    return MechanicGroundTelegraph(shape=m.shape, timer=m.timer)


def contains(shape: MechanicShape, px: float, py: float) -> bool:
    if isinstance(shape, Circle):
        return (px - shape.x) ** 2 + (py - shape.y) ** 2 <= shape.radius**2

    if isinstance(shape, Rectangle):
        half_w, half_h = shape.width / 2, shape.height / 2
        return (
            shape.x - half_w <= px <= shape.x + half_w
            and shape.y - half_h <= py <= shape.y + half_h
        )

    if isinstance(shape, Composite):
        # evaluate children first
        results = [contains(s, px, py) for s in shape.shapes]
        if shape.op is Op.UNION:
            return any(results)
        elif shape.op is Op.INTERSECTION:
            return all(results)
        elif shape.op is Op.DIFFERENCE:
            # first shape minus all others
            return results[0] and not any(results[1:])
        else:
            raise ValueError("Unknown composite op")

    raise TypeError(f"Unsupported shape type: {type(shape)}")


# — some examples


# 1) a “plus” shape: horizontal rect ∪ vertical rect
hor = Rectangle(x=0, y=0, width=50, height=10)
ver = Rectangle(x=0, y=0, width=10, height=50)
plus = Composite(op=Op.UNION, shapes=[hor, ver])

# 2) a “ring”: big circle minus small circle
outer = Circle(x=0, y=0, radius=30)
inner = Circle(x=0, y=0, radius=10)
ring = Composite(op=Op.DIFFERENCE, shapes=[outer, inner])

# 3) a “rounded corner” intersection
c1 = Circle(x=20, y=20, radius=30)
r1 = Rectangle(x=20, y=20, width=40, height=40)
corner = Composite(op=Op.INTERSECTION, shapes=[c1, r1])

# — test

points = [(0, 0), (20, 0), (0, 20), (25, 25), (40, 0), (0, 40)]
print("Plus contains:")
for p in points:
    print(p, contains(plus, *p))

print("\nRing contains:")
for p in [(0, 0), (15, 0), (25, 0), (40, 0)]:
    print(p, contains(ring, *p))

print("\nCorner contains:")
for p in [(20, 20), (40, 20), (20, 40), (50, 50)]:
    print(p, contains(corner, *p))
