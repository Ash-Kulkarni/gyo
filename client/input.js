const A_KEY = 0;
const B_KEY = 1;
const X_KEY = 2;
const Y_KEY = 3;
const LEFT_BUMPER_KEY = 4;
const RIGHT_BUMPER_KEY = 5;
const LEFT_TRIGGER_KEY = 6;
const RIGHT_TRIGGER_KEY = 7;
const SELECT_KEY = 8;
const START_KEY = 9;
const LEFT_STICK_KEY = 10;
const RIGHT_STICK_KEY = 11;
const DPAD_UP_KEY = 12;
const DPAD_DOWN_KEY = 13;
const DPAD_LEFT_KEY = 14;
const DPAD_RIGHT_KEY = 15;
// const HOME_KEY = 16;

export const equippedModules = [
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

export const pollGamepad = () => navigator.getGamepads()[0] || null;

export const parseGamePad = (gp, modules) => {
  if (!gp) return [false, false];

  const [lx, ly] = gp.axes;
  const [rx, ry] = gp.axes.slice(2, 4);
  const moveMag = Math.hypot(lx, ly);
  const aimMag = Math.hypot(rx, ry);

  const clientInput = {
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
    fire: gp.buttons[RIGHT_TRIGGER_KEY]?.pressed ?? false,
    activate_modules: modules
      .filter(({ keymap }) => gp.buttons[keymap]?.pressed)
      .map(({ module_id }) => module_id),
  };

  const eventTriggers = {
    open_menu: gp.buttons[START_KEY]?.pressed,
  };

  return [clientInput, eventTriggers];
};
