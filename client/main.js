import {
  playerInventory,
  sendInput,
  setupSocket,
  socket,
  state,
  playerId,
} from "./net.js";
import { draw } from "./draw/draw.js";
import { handleEditorInput } from "./draw/editor.js";
import { updateDebugOverlay } from "./debug.js";
import { setCurrentView, VIEW, uiState } from "./state.js";
import {
  pollGamepad,
  parseGamePadPlaying,
  parseGamePadEditing,
  equippedModules,
} from "./input.js";

// const playerInventory = [
//   // {
//   //   id: 1,
//   //   name: "Laser Cannon",
//   //   module_id: 20,
//   //   weapon_id: "lc01",
//   //   cooldown: 0,
//   //   max_cooldown: 0.2,
//   //   offset_angle: 0.2,
//   //   distance: 20,
//   //   aim_angle: 0,
//   // },
//   // { id: 2, name: "Shield Generator" },
//   // { id: 3, name: "Engine Module" },
// ];

const handleEventsPlaying = (triggers) => {
  if (triggers.length === 0) return uiState.currentView;
  if (triggers.open_menu) {
    setCurrentView(
      uiState.currentView === VIEW.MAIN_MENU ? VIEW.PLAYING : VIEW.MAIN_MENU,
    );
  } else if (triggers.open_ship_editor) {
    setCurrentView(
      uiState.currentView === VIEW.EDITOR ? VIEW.PLAYING : VIEW.EDITOR,
    );
  }
  return uiState.currentView;
};
const handleEventsEditing = (triggers) => {
  if (triggers.length === 0) return uiState.currentView;
  if (triggers.open_menu) {
    setCurrentView(
      uiState.currentView === VIEW.MAIN_MENU ? VIEW.PLAYING : VIEW.MAIN_MENU,
    );
  } else if (triggers.open_ship_editor) {
    setCurrentView(
      uiState.currentView === VIEW.EDITOR ? VIEW.PLAYING : VIEW.EDITOR,
    );
  }
  handleEditorInput(triggers, state.players[playerId], playerInventory);

  return uiState.currentView;
};

const handleEvents = (triggers) => {
  if (uiState.currentView === VIEW.PLAYING) {
    return handleEventsPlaying(triggers);
  } else if (uiState.currentView === VIEW.EDITOR) {
    return handleEventsEditing(triggers);
  } else if (uiState.currentView === VIEW.MAIN_MENU) {
    return handleEventsPlaying(triggers);
  } else {
    console.warn("Unknown view:", uiState.currentView);
  }
};

// todo: debounce module activations
// todo: switch 'fire' to start and stop fire events
let prevTriggers = {};
const gameLoop = () => {
  const gpInput = pollGamepad();
  let clientInput = {};
  let eventTriggers = {};
  if (uiState.currentView === VIEW.PLAYING) {
    [clientInput, eventTriggers] = parseGamePadPlaying(
      gpInput,
      equippedModules,
    );
  } else if (uiState.currentView === VIEW.EDITOR) {
    [clientInput, eventTriggers] = parseGamePadEditing(gpInput);
  } else if (uiState.currentView === VIEW.MAIN_MENU) {
    [clientInput, eventTriggers] = parseGamePadPlaying(
      gpInput,
      equippedModules,
    );
  } else {
    console.warn("Unknown view:", uiState.currentView);
  }

  const triggers = {};
  for (const key in eventTriggers) {
    triggers[key] = eventTriggers[key] && !prevTriggers[key];
  }
  prevTriggers = eventTriggers;

  sendInput(clientInput);
  const view = handleEvents(triggers);
  draw(view, state, clientInput, playerInventory);
  updateDebugOverlay(clientInput);
  requestAnimationFrame(gameLoop);
};

setupSocket(gameLoop);
