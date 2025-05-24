from dataclasses import dataclass
from typing import Union, List, Any
from enum import Enum
import math


@dataclass
class Sector:
    x: float
    y: float
    radius: float
    start_angle: float  # in radians
    end_angle: float  # in radians


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


MechanicShape = Union[
    Circle,
    Rectangle,
    Sector,
    Composite,
]


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

    if isinstance(shape, Sector):
        # 1) inside radius?
        dx, dy = px - shape.x, py - shape.y
        dist2 = dx * dx + dy * dy
        if dist2 > shape.radius**2:
            return False

        # 2) angle within [start, end]?
        ang = math.atan2(dy, dx)  # [-pi,pi]
        # normalize to [0,2pi)
        if ang < 0:
            ang += 2 * math.pi
        sa = shape.start_angle % (2 * math.pi)
        ea = shape.end_angle % (2 * math.pi)

        if sa <= ea:
            return sa <= ang <= ea
        else:
            # wraps around zero
            return ang >= sa or ang <= ea

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

if __name__ == "__main__":
    # plus‐shape
    hor = Rectangle(x=0, y=0, width=50, height=10)
    ver = Rectangle(x=0, y=0, width=10, height=50)
    plus = Composite(op=Op.UNION, shapes=[hor, ver])

    # ring
    outer = Circle(x=0, y=0, radius=30)
    inner = Circle(x=0, y=0, radius=10)
    ring = Composite(op=Op.DIFFERENCE, shapes=[outer, inner])

    # quarter‐circle sector (0° → 90°)
    quarter = Sector(x=0, y=0, radius=20, start_angle=0, end_angle=math.pi / 2)

    # test points
    pts = [(0, 0), (20, 0), (0, 20), (15, 15), (-5, 5), (5, -5)]
    print("Plus contains:")
    for p in pts:
        print(f"  {p}: {contains(plus, *p)}")

    print("\nRing contains:")
    for p in [(0, 0), (15, 0), (25, 0), (0, 15), (0, 25)]:
        print(f"  {p}: {contains(ring, *p)}")

    print("\nQuarter-sector contains:")
    for p in pts:
        print(f"  {p}: {contains(quarter, *p)}")
