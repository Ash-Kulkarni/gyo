
def dist_sq(x1, y1, x2, y2):
    return (x1 - x2)**2 + (y1 - y2)**2


def check_bullet_collisions(bullets, enemies):
    hit_radius_sq = 16  # ~4 px hit radius

    dead_enemies = []
    live_bullets = []

    for bullet in bullets:
        hit = False
        for enemy in enemies:
            if dist_sq(bullet["x"], bullet["y"], enemy["x"], enemy["y"]) < hit_radius_sq:
                enemy["hp"] -= 1  # simple damage
                hit = True
                break
        if not hit:
            live_bullets.append(bullet)

    # Cull dead enemies
    for e in enemies:
        if e["hp"] <= 0:
            dead_enemies.append(e)
    enemies[:] = [e for e in enemies if e["hp"] > 0]

    return live_bullets, dead_enemies

