import { state, socket, playerId } from "./net.js";

const deepPrintObject = (obj, depth = 0) => {
  if (depth > 2) return "...";
  if (typeof obj !== "object" || obj === null) return String(obj);
  if (Array.isArray(obj)) {
    return `[${obj.map((item) => deepPrintObject(item, depth + 1)).join(", ")}]`;
  }
  const entries = Object.entries(obj)
    .map(([key, value]) => `${key}: ${deepPrintObject(value, depth + 1)}`)
    .join(", ");
  return `{${entries}}`;
};

export function updateDebugOverlay(input) {
  const debug = document.getElementById("debug");

  try {
    if (!state.players) return;
    const player = state.players[playerId];
    const lines = [
      `Players: ${Object.keys(state.players).length}`,
      player
        ? `You: x=${player.x.toFixed(1)} y=${player.y.toFixed(1)}`
        : "You: -",
      player ? `Angle: ${((player.a * 180) / Math.PI).toFixed(1)}°` : "",
      "Input: ",
      deepPrintObject(input),
      `Ping: ${socket.readyState === 1 ? "🟢" : "🔴"}`,
    ];
    debug.textContent = lines.join("\n");
  } catch (e) {
    console.error("Error updating debug overlay:", e);
    debug.textContent = "Error: " + e.message;
  }
}
