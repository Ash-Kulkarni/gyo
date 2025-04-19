const A_KEY = 0;
const B_KEY = 1;
const X_KEY = 2;

const equippedModules = [
  {
    module_id: 1,
    type: "boost",
    keymap: A_KEY,
  },
  {
    module_id: 2,
    type: "boost",
    keymap: B_KEY,
  },
  {
    module_id: 3,
    type: "shield",
    keymap: X_KEY,
  },
];

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
    fire: gp.buttons[7]?.pressed ?? false,
    activate_modules: equippedModules
      .filter(({ keymap }) => gp.buttons[keymap]?.pressed)
      .map(({ module_id }) => module_id),
  };
}
