export let socket = null;
export let playerId = null;
export let state = {};
export let playerInventory = [];

/**
 * Safely closes the existing WebSocket connection if it exists.
 */
function closeSocket() {
  if (!socket) return
  socket.onopen = null;
  socket.onmessage = null;
  socket.onerror = null;
  socket.onclose = null;
  if (socket.readyState === WebSocket.OPEN || socket.readyState === WebSocket.CONNECTING) {
    socket.close();
  }
  socket = null;
};

/**
 * Sends input to the server via WebSocket.
 * @param {Object} input - The input object to send.
 */
export function sendInput(input) {
  if (!socket || socket.readyState !== WebSocket.OPEN) return;
  if (!input) return;
  const filteredInput = Object.fromEntries(
    Object.entries(input).filter(([_, value]) => value !== false)
  );
  socket.send(JSON.stringify(filteredInput));
}

/**
 * Sets up the WebSocket connection and event handlers.
 * @param {Function} startGameLoop - Callback to start the game loop.
 */
export function setupSocket(startGameLoop) {
  closeSocket(); // Ensure any existing socket is closed before creating a new one

  socket = new WebSocket("ws://localhost:8000/ws");
  if (!socket) {
    console.error("❗ Failed to create WebSocket connection");
    return;
  }

  socket.onopen = () => {
    console.log("✅ Connected to server");
    startGameLoop();
  };

  socket.onmessage = async (event) => {
    try {
      state = JSON.parse(event.data);
      if (!state || Object.keys(state).length === 0) {
        console.warn("Received empty state from server");
      }
      if (state.type === "hello") {
        playerId = state.pid;
        playerInventory = await getInventory(playerId);
      }
    } catch (error) {
      console.error("Error processing server message:", error);
    }
  };

  socket.onerror = (error) => {
    console.error("❗ Socket error:", error);
  };

  socket.onclose = () => {
    console.warn("🔌 Disconnected from server");
  };
}

/**
 * Fetches the player's inventory from the server.
 * @param {string} pid - The player ID.
 * @returns {Promise<Array>} The player's inventory.
 */
export async function getInventory(pid) {
  try {
    const url = `http://localhost:8000/inventory/${pid}`;
    const response = await fetch(url, { method: "GET" });
    if (!response.ok) {
      console.error("Failed to fetch inventory:", response);
      throw new Error("Network response was not ok");
    }
    return await response.json();
  } catch (error) {
    console.error("Error fetching inventory:", error);
    return [];
  }
}
