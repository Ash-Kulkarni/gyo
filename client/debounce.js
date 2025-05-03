import { sendInput } from "./net.js";
import { EDITOR_MODE, editorState } from "./draw/editor.js";
import { EDITOR_KEYMAP } from "./input.js";

let prevEvents = {};
let debounceTimers = {};
let repeatTimers = {};

export const getRisingEdge = (triggers, mode) => {
  const edges = {};
  const debounceSensitivity = mode === 'EDITOR' ? 200 : 0; // 200ms debounce for EDITOR mode
  const repeatKeys = mode === 'EDITOR' ? [
    EDITOR_KEYMAP.DPAD_UP_KEY,
    EDITOR_KEYMAP.DPAD_DOWN_KEY,
    EDITOR_KEYMAP.DPAD_LEFT_KEY,
    EDITOR_KEYMAP.DPAD_RIGHT_KEY
  ].map(k => k.toString()) : [];

  for (const key in triggers) {
    const isDebounced = debounceTimers[key] && (Date.now() - debounceTimers[key]) < debounceSensitivity;

    if (triggers[key]) {
      if (!prevEvents[key] && !isDebounced) {
        // Rising edge: key was just pressed
        edges[key] = true;
        debounceTimers[key] = Date.now();
      } else if ((EDITOR_MODE.AIM_EDIT === editorState.mode || EDITOR_MODE.POSITION_EDIT === editorState.mode) && repeatKeys.includes(key)) {
        // Handle held keys for repeatKeys
        if (!repeatTimers[key]) {
          repeatTimers[key] = setInterval(() => {
            sendInput({ [key]: true }); // Send repeated input
          }, debounceSensitivity);
        }
        edges[key] = true; // Ensure the key is marked as active
      }
    } else {
      // Key is not pressed
      edges[key] = false;

      // Clear repeat timer if key is released
      if (repeatTimers[key]) {
        clearInterval(repeatTimers[key]);
        delete repeatTimers[key];
      }
    }
  }

  prevEvents = { ...triggers };
  return edges;
};
