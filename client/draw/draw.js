const canvas = document.getElementById("game");
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

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

export function draw(view, state, input) {
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
    drawBaysAtPosition(players[pid], x, y, color);
    // drawBays(players[pid], color);
    if (pid === playerId) {
      drawThrust(x, y, a || 0, input?.move);
    }
  }

  drawBullets(bullets);
  ctx.restore();
  drawUIOverlay(view, state, input, players[playerId]);
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
function drawUIOverlay(view, state, input, player) {
  ctx.save();
  ctx.translate(0, 0);

  if (view === "main_menu") {
    drawMainMenu();
  } else if (view === "editor") {
    drawShipEditorBackground();
    drawShipEditorView(ctx, player);
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
function drawBaysAtPosition(player, x, y, color) {
  const bays = player.bays || [];
  const baseAngle = player.a || 0;

  for (const bay of bays) {
    const angleOffset = bay.offset_angle ?? 0;
    const dist = bay.distance ?? 20;

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

function drawBays(player, color) {
  const bays = player.bays || [];
  const baseAngle = player.a || 0;

  for (const bay of bays) {
    const angleOffset = bay.offset_angle ?? 0;
    const dist = bay.distance ?? 20;

    const angle = baseAngle + angleOffset;
    const bx = player.x + Math.cos(angle) * dist;
    const by = player.y + Math.sin(angle) * dist;

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
    ctx.shadowBlur = 8;
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

export function drawShipEditorView(ctx, ship, inventory = undefined) {
  const panelY = 40;
  const panelW = 320;
  const panelH = 360;
  const padding = 16;
  const lineHeight = 22;

  const invX = 520;
  const eqX = 880;
  const shipX = 160;
  const shipY = canvas.height / 2;

  const inv = inventory || [
    { id: 1, name: "Laser Cannon" },
    { id: 2, name: "Shield Generator" },
    { id: 3, name: "Engine Module" },
  ];

  drawPanel(shipX - 140, panelY, 280, panelH, "Ship Preview");
  drawShipPreview(ctx, ship, shipX, shipY);

  drawPanel(invX, panelY, panelW, panelH, "Inventory");
  ctx.save();
  ctx.fillStyle = "#bbb";
  ctx.font = "13px monospace";
  inv.forEach((item, i) => {
    const y = panelY + 48 + i * lineHeight;
    ctx.fillText(`${item.name} (id: ${item.id})`, invX + padding, y);
    drawDivider(invX + padding, y + 4, panelW - padding * 2);
  });
  ctx.restore();

  drawPanel(eqX, panelY, panelW, panelH, "Equipped");
  ctx.save();
  ctx.fillStyle = "#bbb";
  ctx.font = "13px monospace";
  ship.modules.forEach((mod, i) => {
    const y = panelY + 48 + i * lineHeight;
    ctx.fillText(
      `${mod.name} → angle ${mod.offset_angle}°, dist ${mod.distance}`,
      eqX + padding,
      y,
    );
    drawDivider(eqX + padding, y + 4, panelW - padding * 2);
  });
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
function drawShipPreview(ctx, ship, centerX, centerY) {
  drawTriangle(centerX, centerY, ship.a || 0, "cyan");
  drawBaysAtPosition(ship, centerX, centerY, "cyan");
}

function drawPanel(x, y, w, h, title) {
  ctx.save();
  ctx.fillStyle = "rgba(15, 15, 20, 0.9)";
  ctx.shadowColor = "#0ff";
  ctx.shadowBlur = 8;
  ctx.fillRect(x, y, w, h);

  ctx.strokeStyle = "rgba(200,255,255,0.2)";
  ctx.lineWidth = 1.5;
  ctx.strokeRect(x, y, w, h);

  ctx.fillStyle = "#0ff";
  ctx.font = "bold 16px sans-serif";
  ctx.fillText(title, x + 12, y + 24);
  ctx.restore();
}
