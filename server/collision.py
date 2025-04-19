from .shared.shapes import SHAPES

import math


def dist_sq(x1, y1, x2, y2):
    return (x1 - x2)**2 + (y1 - y2)**2


def check_bullet_collisions(bullets, enemies, scoreboard):
    dead_enemies = []
    live_bullets = []

    for bullet in bullets:
        hit = False
        circle = {
            "x": bullet["x"],
            "y": bullet["y"],
            "r": bullet.get("radius")
        }
        for enemy in enemies:
            ex, ey = enemy["x"], enemy["y"]

            dx = circle["x"] - ex
            dy = circle["y"] - ey
            if dx * dx + dy * dy > (circle["r"]+10 ** 2):
                continue

            shape_id = enemy.get("shape_id")
            if not shape_id:
                raise ValueError("Enemy shape_id is missing")
            verts = SHAPES.get(shape_id)
            if not verts:
                raise ValueError(f"Shape {shape_id} not found in SHAPES")

            angle = enemy.get("a", 0)

            if sat_circle_vs_polygon(circle, verts, ex, ey, angle):
                enemy["hp"] -= 1
                hit = True
                if enemy["hp"] <= 0:
                    scoreboard[bullet["from"]]["kills"] += 1
                    dead_enemies.append(enemy)
                    # print(f"Enemy {enemy} killed by bullet {bullet}")
                break

        if not hit:
            live_bullets.append(bullet)

    enemies[:] = [e for e in enemies if e["hp"] > 0]
    # dead_enemies = [e for e in enemies if e["hp"] <= 0]
    return live_bullets, dead_enemies


def handle_enemy_player_collisions(players, enemies):
    for pid, player in players.items():
        px, py = player["x"], player["y"]
        for enemy in enemies:
            dx = enemy["x"] - px
            dy = enemy["y"] - py
            dist_sq = dx * dx + dy * dy
            if dist_sq < (20 ** 2):  # collision range
                player["hp"] -= 1  # basic contact damage


def rotate_point(px, py, angle):
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)
    return (px * cos_a - py * sin_a, px * sin_a + py * cos_a)


def translate_and_rotate_polygon(vertices, x, y, angle):
    return [(x + dx, y + dy) for (dx, dy) in [rotate_point(px, py, angle) for (px, py) in vertices]]


def dot(v1, v2):
    return v1[0]*v2[0] + v1[1]*v2[1]


def project_polygon(axis, vertices):
    projections = [dot(v, axis) for v in vertices]
    return min(projections), max(projections)


def project_circle(axis, cx, cy, radius):
    center_proj = dot((cx, cy), axis)
    return center_proj - radius, center_proj + radius


def normalize(vx, vy):
    length = math.hypot(vx, vy)
    return (vx / length, vy / length) if length != 0 else (0, 0)


def polygons_overlap(poly_proj, circle_proj):
    return not (poly_proj[1] < circle_proj[0] or circle_proj[1] < poly_proj[0])


def sat_circle_vs_polygon(circle, polygon_vertices, px, py, angle):
    world_poly = translate_and_rotate_polygon(polygon_vertices, px, py, angle)

    for i in range(len(world_poly)):
        p1 = world_poly[i]
        p2 = world_poly[(i + 1) % len(world_poly)]
        edge = (p2[0] - p1[0], p2[1] - p1[1])
        axis = normalize(-edge[1], edge[0])

        poly_proj = project_polygon(axis, world_poly)
        circle_proj = project_circle(
            axis, circle["x"], circle["y"], circle["r"])

        if not polygons_overlap(poly_proj, circle_proj):
            return False

    closest_point = min(world_poly, key=lambda v: (
        v[0] - circle["x"])**2 + (v[1] - circle["y"])**2)
    axis_to_circle = normalize(
        closest_point[0] - circle["x"], closest_point[1] - circle["y"])
    poly_proj = project_polygon(axis_to_circle, world_poly)
    circle_proj = project_circle(
        axis_to_circle, circle["x"], circle["y"], circle["r"])

    return polygons_overlap(poly_proj, circle_proj)

# # Example usage
# circle = {"x": 5, "y": 5, "r": 3}
# triangle = [(0, -10), (6, 8), (-6, 8)]
# enemy_x, enemy_y, enemy_angle = 5, 5, 0
#
# sat_circle_vs_polygon(circle, triangle, enemy_x, enemy_y, enemy_angle)
