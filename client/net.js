export let socket = null;
export let playerId = null;
export let state = {};
export let playerInventory = [];

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

  socket.onmessage = async (event) => {
    // console.log("📩 Message from server:", event.data);
    state = JSON.parse(event.data);
    // console.log({ state });
    if (state.type === "hello") {
      playerId = state.pid;
      playerInventory = await getInventory(playerId);
    }
  };

  socket.onerror = (e) => {
    console.error("❗ Socket error:", e);
  };

  socket.onclose = () => {
    console.warn("🔌 Disconnected from server");
  };
}

export function getInventory(pid) {
  try {
    const url = "http://localhost:8000/inventory/" + pid;
    // implement cors header

    return fetch(url, { method: "GET" }).then((response) => {
      if (!response.ok) {
        console.log({ response });
        throw new Error("Network response was not ok");
      }
      return response.json();
    });
  } catch (error) {
    console.error("Error fetching inventory:", error);
    return [];
  }
}
