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
import { pollGamepad, parseGamepad } from "./input.js";
import { setupAudio } from "./audio.js";
import { getRisingEdge } from "./debounce.js";


// Handles client-side events based on gamepad input, such as opening menus or switching views.
const handleEvents = (triggers) => {
  if (!state?.players || !playerId) return uiState.currentView;

  if (triggers?.open_menu) {
    setCurrentView(uiState.currentView === VIEW.MAIN_MENU ? VIEW.PLAYING : VIEW.MAIN_MENU)
  }

  if (triggers?.open_ship_editor) {
    setCurrentView(uiState.currentView === VIEW.EDITOR ? VIEW.PLAYING : VIEW.EDITOR);
  }

  if (uiState.currentView === VIEW.EDITOR) {
    const player = state.players[playerId];
    const equippedModuleIds = player.modules.map(({ module_id }) => module_id);
    const unequippedInventory = playerInventory.filter(
      inv => !equippedModuleIds.includes(inv.module_id),
    );
    handleEditorInput(triggers, player, unequippedInventory);
  }
  return uiState.currentView;
};


const gameLoop = () => {
  const gp = pollGamepad();
  if (!gp) {
    requestAnimationFrame(gameLoop);
    return;
  }
  const mode = uiState.currentView === VIEW.EDITOR ? 'EDITOR' : uiState.currentView === VIEW.PLAYING ? 'PLAYING' : 'MAIN_MENU';
  const { clientInput, eventTriggers } = parseGamepad(mode, gp);
  const triggers = getRisingEdge(eventTriggers, mode);

  sendInput(clientInput);
  const view = handleEvents(triggers);
  draw(view, state, clientInput, playerInventory);
  updateDebugOverlay(clientInput);
  requestAnimationFrame(gameLoop);
};

setupAudio();
setupSocket(gameLoop);
