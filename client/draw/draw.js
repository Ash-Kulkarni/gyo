const canvas = document.getElementById("game");
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;
import { editorState, EDITOR_MODE } from "./editor.js";

window.addEventListener("resize", () => {
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
});

const ctx = canvas.getContext("2d");
import { playerId } from "./../net.js";
import { SHAPES } from "./../shared/shapes.js";

export function drawTriangle(x, y, angle, color) {
  ctx.save();
  ctx.translate(x, y);
  ctx.rotate(angle + Math.PI / 2);
  ctx.beginPath();
  ctx.moveTo(0, -10);
  ctx.lineTo(6, 8);
  ctx.lineTo(-6, 8);
  ctx.closePath();
  ctx.fillStyle = color;
  ctx.shadowColor = color;
  ctx.shadowBlur = 15;
  ctx.shadowOffsetX = Math.cos(angle) * 2;
  ctx.shadowOffsetY = Math.sin(angle) * 2;
  ctx.fill();
  ctx.restore();
}

function drawThrust(x, y, angle, isMoving) {
  if (!isMoving) return;

  ctx.save();
  ctx.translate(x, y);
  ctx.rotate(angle + Math.PI / 2); // face forward

  ctx.beginPath();
  ctx.moveTo(0, 10);
  ctx.lineTo(3, 18);
  ctx.lineTo(-3, 18);
  ctx.closePath();

  ctx.fillStyle = "rgba(0, 255, 255, 0.4)";
  ctx.shadowColor = "cyan";
  ctx.shadowBlur = 20;
  ctx.fill();

  ctx.restore();
}

function drawWorldBorder() {
  const WORLD_SIZE = 2000;
  const t = Date.now() / 1000;
  const alpha = 0.3 + Math.sin(t * 2) * 0.2;

  // ctx.strokeStyle = "#444";
  ctx.strokeStyle = `rgba(180,180,180,${alpha})`;
  ctx.lineWidth = 2;
  ctx.shadowColor = "#000";
  ctx.shadowBlur = 10;

  ctx.strokeRect(-WORLD_SIZE, -WORLD_SIZE, WORLD_SIZE * 2, WORLD_SIZE * 2);
}
function drawBackground(camX, camY) {
  const spacing = 50;
  const dotRadius = 1.2;
  const cols = Math.ceil(canvas.width / spacing) + 2;
  const rows = Math.ceil(canvas.height / spacing) + 2;

  const offsetX = camX % spacing;
  const offsetY = camY % spacing;

  ctx.fillStyle = "#222"; // soft, faint dots
  for (let i = -1; i < cols; i++) {
    for (let j = -1; j < rows; j++) {
      const x = i * spacing - offsetX;
      const y = j * spacing - offsetY;
      ctx.beginPath();
      ctx.arc(x, y, dotRadius, 0, 2 * Math.PI);
      ctx.fill();
    }
  }
}

function drawEnemies(enemies) {
  for (const e of enemies) {
    drawPolygon(e.x, e.y, e.a || 0, SHAPES[e.shape_id], e.colour);
  }
}

export function draw(view, state, input, inventory) {
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  const players = state.players || {};
  const bullets = state.bullets || [];
  const enemies = state.enemies || [];
  const player = players[playerId];
  if (!player) return;
  const camX = player.x - canvas.width / 2;
  const camY = player.y - canvas.height / 2;
  drawBackground(camX, camY);
  ctx.save();
  ctx.translate(-camX, -camY); // Shift world around player
  drawWorldBorder();
  drawEnemies(enemies);
  for (const pid in players) {
    const { x, y, a } = players[pid];
    const color = pid === playerId ? "cyan" : "magenta";
    drawTriangle(x, y, a || 0, color);
    drawModsAtPosition(players[pid], x, y, color);
    if (pid === playerId) {
      drawThrust(x, y, a || 0, input?.move);
    }
  }

  drawBullets(bullets);
  ctx.restore();
  drawUIOverlay(view, state, input, players[playerId], inventory);
}

function drawMainMenu() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ctx.fillStyle = "#111";
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  ctx.fillStyle = "white";
  ctx.font = "24px sans-serif";
  ctx.fillText("Paused", canvas.width / 2 - 40, canvas.height / 2);
  ctx.fillText(
    "Press START to return",
    canvas.width / 2 - 100,
    canvas.height / 2 + 40,
  );
}
function drawUIOverlay(view, state, input, player, inventory) {
  if (view === "playing") return;
  ctx.save();
  ctx.translate(0, 0);

  if (view === "main_menu") {
    drawMainMenu();
  } else if (view === "editor") {
    drawShipEditorBackground();
    drawShipEditorView(ctx, player, inventory);
  } else if (view === "shop") {
    // drawShopUI();
  } else console.warn("Unknown view:", view);

  ctx.restore();
}

const drawShipEditorBackground = () => {
  ctx.save();
  ctx.fillStyle = "rgba(20, 20, 30, 0.8)";
  ctx.fillRect(0, 0, canvas.width, canvas.height);
  ctx.restore();
};

function drawBullets(bullets) {
  for (const b of bullets) {
    ctx.beginPath();
    ctx.arc(b.x, b.y, b.radius, 0, 2 * Math.PI);
    ctx.shadowColor = "white";
    ctx.shadowBlur = 15;
    ctx.fillStyle = "white";
    ctx.fill();
  }
}
function drawModsAtPosition(player, x, y, color) {
  const weapons = player.modules.filter(({ weapon_id }) => weapon_id) || [];
  const baseAngle = player.a || 0;

  for (const w of weapons) {
    const angleOffset = w.offset_angle ?? 0;
    const dist = w.distance ?? 20;

    const angle = baseAngle + angleOffset;
    const bx = x + Math.cos(angle) * dist;
    const by = y + Math.sin(angle) * dist;

    ctx.save();
    ctx.translate(bx, by);
    ctx.rotate(baseAngle + Math.PI / 2);
    ctx.beginPath();
    ctx.moveTo(0, -3);
    ctx.lineTo(4, 3);
    ctx.lineTo(-4, 3);
    ctx.closePath();
    ctx.fillStyle = color;
    ctx.shadowColor = color;
    ctx.shadowBlur = 6;
    ctx.fill();
    ctx.restore();
  }
}

function drawPolygon(x, y, angle, verts, color) {
  ctx.save();
  ctx.translate(x, y);
  ctx.rotate(angle);
  ctx.beginPath();
  ctx.moveTo(verts[0][0], verts[0][1]);
  for (let i = 1; i < verts.length; i++) {
    ctx.lineTo(verts[i][0], verts[i][1]);
  }
  ctx.closePath();

  ctx.fillStyle = `${color}33`; // transparent fill
  ctx.fill();
  // Glow effect
  ctx.strokeStyle = color;
  ctx.shadowColor = color;
  ctx.shadowBlur = 20;
  ctx.lineWidth = 2;

  ctx.stroke();
  ctx.restore();
}

// Minimal, muted panel styling
function drawPanel(x, y, w, h, title) {
  ctx.save();
  ctx.fillStyle = "rgba(30, 30, 35, 0.85)";
  ctx.shadowColor = "rgba(0, 0, 0, 0.4)";
  ctx.shadowBlur = 6;
  ctx.fillRect(x, y, w, h);

  ctx.strokeStyle = "rgba(120, 120, 130, 0.4)";
  ctx.lineWidth = 1;
  ctx.strokeRect(x, y, w, h);

  ctx.fillStyle = "#aaa";
  ctx.font = "bold 14px monospace";
  ctx.fillText(title, x + 12, y + 22);
  ctx.restore();
}

function drawDivider(x, y, width) {
  ctx.save();
  ctx.strokeStyle = "rgba(255,255,255,0.05)";
  ctx.beginPath();
  ctx.moveTo(x, y);
  ctx.lineTo(x + width, y);
  ctx.stroke();
  ctx.restore();
}

// Ship‑editor UI panels at bottom corners
export function drawShipEditorView(ctx, ship, inventory = []) {
  const padding = 16;
  const lineHeight = 22;
  const panelW = 360;
  const panelH = 220;
  const panelY = canvas.height - panelH - 40;

  const invX = 40;
  const eqX = canvas.width - panelW - 40;
  const { mode, inventoryIndex, equippedIndex } = editorState;

  // Inventory panel
  drawPanel(invX, panelY, panelW, panelH, "Inventory");
  ctx.save();
  ctx.fillStyle = "#bbb";
  ctx.font = "13px monospace";
  inventory.forEach((item, i) => {
    const y = panelY + 42 + i * lineHeight;
    if (mode === EDITOR_MODE.INVENTORY && i === inventoryIndex) {
      ctx.fillStyle = "rgba(200, 200, 200, 0.15)";
      ctx.fillRect(invX + padding / 2, y - 12, panelW - padding, lineHeight);
    }
    ctx.fillText(`${item.name} (id: ${item.id})`, invX + padding, y);
    drawDivider(invX + padding, y + 4, panelW - padding * 2);
  });
  ctx.restore();

  // Equipped panel
  drawPanel(eqX, panelY, panelW, panelH, "Equipped");
  ctx.save();
  ctx.fillStyle = "#bbb";
  ctx.font = "13px monospace";
  ship.modules.forEach((mod, i) => {
    const y = panelY + 42 + i * lineHeight;
    if (
      (mode === EDITOR_MODE.EQUIPPED ||
        mode === EDITOR_MODE.POSITION_EDIT ||
        mode === EDITOR_MODE.AIM_EDIT) &&
      i === equippedIndex
    ) {
      ctx.fillStyle = "rgba(200, 200, 200, 0.15)";
      ctx.fillRect(eqX + padding / 2, y - 12, panelW - padding, lineHeight);
    }
    ctx.fillText(
      `${mod.name} → θ:${mod.offset_angle?.toFixed(1)}°, r:${mod.distance}`,
      eqX + padding,
      y,
    );
    drawDivider(eqX + padding, y + 4, panelW - padding * 2);
  });
  ctx.restore();
}
