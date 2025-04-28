
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


/**
* @returns {Gamepad | null} 
**/
export const pollGamepad = () => navigator.getGamepads()[0] || null;


/**
* @typedef startSelectEventTriggers
* @type {Object}
* @property {boolean} open_menu
* @property {boolean} open_ship_editor
**/

/** 
* @param {Gamepad} gp
* @returns {startSelectEventTriggers}
**/
const getStartSelectEventTriggers = (gp) =>
({
  open_menu: gp.buttons[START_KEY]?.pressed,
  open_ship_editor: gp.buttons[SELECT_KEY]?.pressed,
})

const getPlayerFiring = (gp) => ({
  fire: gp.buttons[RIGHT_TRIGGER_KEY]?.pressed ?? false
})

const getPlayerAim = (gp) => {
  const [rx, ry] = gp.axes.slice(2, 4);
  const aimMag = Math.hypot(rx, ry);
  if (aimMag > 0.3) {
    return {
      aim: {
        x: rx,
        y: ry,
      }
    }
  }
  return {}
}

const getPlayerMovement = (gp) => {
  const [lx, ly] = gp.axes;
  const moveMag = Math.hypot(lx, ly);
  if (moveMag > 0.2) {
    return {
      move: {
        x: lx * 2,
        y: ly * 2,
      }
    }
  }
  return {
    move: {
      x: 0,
      y: 0
    }
  }
}

/**
* @typedef clientGameplayInput
* @type {Object}
* @property {Object} move
* @property {number} move.x
* @property {number} move.y
* @property {Object} [aim]
* @property {number} [aim.x]
* @property {number} [aim.y]
* @property {boolean} fire
**/


export const EDITOR_KEYMAP = {
  DPAD_UP_KEY,
  DPAD_DOWN_KEY,
  DPAD_LEFT_KEY,
  DPAD_RIGHT_KEY,
  A_KEY,
  B_KEY,
  RIGHT_BUMPER_KEY,
  LEFT_BUMPER_KEY,
};

const getEditorInput = (gp) => {
  const eventTriggers = {};

  for (const key of Object.values(EDITOR_KEYMAP)) {
    if (gp.buttons[key]?.pressed) {
      eventTriggers[key] = true;
    }
  }
  return eventTriggers;
}

export const parseGamepad = (mode, gp) => {
  const clientInput = {
    ...getPlayerMovement(gp),
    ...getPlayerFiring(gp),
    ...getPlayerAim(gp)
  }

  let eventTriggers = getStartSelectEventTriggers(gp);
  if (mode === 'EDITOR') {
    eventTriggers = {
      ...eventTriggers,
      ...getEditorInput(gp),
    }
  }

  return {
    clientInput,
    eventTriggers
  }

}
