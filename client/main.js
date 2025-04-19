import { sendInput, setupSocket, socket, state, playerId } from "./net.js";
import { draw } from "./draw/draw.js";
import { updateDebugOverlay } from "./debug.js";
import { setCurrentView, VIEW, uiState } from "./state.js";
import { pollGamepad, parseGamePad, equippedModules } from "./input.js";

const handleEvents = (triggers) => {
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

const gameLoop = () => {
  const gpInput = pollGamepad();
  const [clientInput, eventTriggers] = parseGamePad(gpInput, equippedModules);
  sendInput(clientInput);
  const view = handleEvents(eventTriggers);
  draw(view, state, clientInput);
  updateDebugOverlay(clientInput);
  requestAnimationFrame(gameLoop);
};

setupSocket(gameLoop);
