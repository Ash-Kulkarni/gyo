import { pollGamepad } from "./input.js";
import { sendInput, setupSocket, socket, state, playerId } from "./net.js";
import { draw } from "./draw.js";
import { updateDebugOverlay } from "./debug.js";

function gameLoop() {
  const input = pollGamepad();
  sendInput(input);
  draw(state, input);
  updateDebugOverlay(input);
  requestAnimationFrame(gameLoop);
}

setupSocket(gameLoop);
