export let socket = null;
export let playerId = null;
export let state = {};

export function sendInput(input) {
  if (socket.readyState !== WebSocket.OPEN) return;
  if (!input) return;
  input = Object.entries(input).filter(([k, v]) => v !== false);
  input = Object.fromEntries(input);
  socket.send(JSON.stringify(input));
}

export function setupSocket(startGameLoop) {
  socket = new WebSocket("ws://localhost:8000/ws");

  socket.onconnect = () => {
    console.log("✅ Connected to server");
    socket.send(JSON.stringify({ type: "ping" }));
  };

  socket.onopen = () => {
    console.log("✅ Connected to server");
    startGameLoop();
  };

  socket.onmessage = (event) => {
    // console.log("📩 Message from server:", event.data);
    state = JSON.parse(event.data);
    // console.log({ state });
    if (state.type === "hello") {
      playerId = state.pid;
    }
  };

  socket.onerror = (e) => {
    console.error("❗ Socket error:", e);
  };

  socket.onclose = () => {
    console.warn("🔌 Disconnected from server");
  };
}
