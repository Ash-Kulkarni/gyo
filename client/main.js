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
import { pollGamepad, parseGamepad, EDITOR_KEYMAP } from "./input.js";


const audioCtx = new (window.AudioContext || window.webkitAudioContext)();

let bgBuffer, bgSource, bgGain;
async function loadBackgroundLoop() {
  const resp = await fetch('base_loop_1.wav');
  const arrayBuf = await resp.arrayBuffer();
  bgBuffer = await audioCtx.decodeAudioData(arrayBuf);
}
function playBackgroundLoop() {
  bgSource = audioCtx.createBufferSource();
  bgGain = audioCtx.createGain();
  bgSource.buffer = bgBuffer;
  bgSource.loop = true;
  bgGain.gain.value = 0.8;
  bgSource.connect(bgGain).connect(audioCtx.destination);
  bgSource.start();
}
document.addEventListener('click', () => {
  audioCtx.resume().then(() => {
    if (bgBuffer && !bgSource) playBackgroundLoop();
  });
}, { once: true });
loadBackgroundLoop();


let prevEvents = {};
let debounceTimers = {};
let repeatTimers = {};

const getRisingEdge = (triggers, mode) => {
  const edges = {};
  const debounceSensitivity = mode === 'EDITOR' ? 100 : 0;
  const repeatKeys = mode === 'EDITOR' ? [
    EDITOR_KEYMAP.DPAD_UP_KEY, EDITOR_KEYMAP.DPAD_DOWN_KEY, EDITOR_KEYMAP.DPAD_LEFT_KEY, EDITOR_KEYMAP.DPAD_RIGHT_KEY
  ].map(k => k.toString()) : [];
  console.log({ triggers })
  console.log({ repeatKeys })
  for (const key in triggers) {
    key
    console.log({ key })
    const isDebounced = debounceTimers[key] && (Date.now() - debounceTimers[key]) < debounceSensitivity;

    if (triggers[key] && !prevEvents[key] && !isDebounced) {
      edges[key] = true;
      debounceTimers[key] = Date.now();
    } else if (repeatKeys.includes(key)) {
      if (!repeatTimers[key]) {

        edges[key] = true;
        repeatTimers[key] = setInterval(() => {
          edges[key] = true;
        }, 100);

      }
    }
    else {
      edges[key] = false;
      if (repeatTimers[key]) {
        clearInterval(repeatTimers[key]);
        delete repeatTimers[key];
      }

    }
  }
  prevEvents = { ...triggers };
  console.log({ edges })
  return edges;
};

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

setupSocket(gameLoop);
