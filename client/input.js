export function pollGamepad() {
  const gp = navigator.getGamepads()[0];
  if (!gp) return null;

  const [lx, ly] = gp.axes;
  const [rx, ry] = gp.axes.slice(2, 4);
  const moveMag = Math.hypot(lx, ly);
  const aimMag = Math.hypot(rx, ry);

  return {
    move:
      moveMag > 0.2
        ? {
            x: lx * 2,
            y: ly * 2,
          }
        : false,
    aim:
      aimMag > 0.3
        ? {
            x: rx,
            y: ry,
          }
        : false,
    dash: gp.buttons[0]?.pressed ?? false,
    fire: gp.buttons[7]?.pressed ?? false,
  };
}
