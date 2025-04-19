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
// const nodes = createSectorMap(30, 1200, 500);
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
    drawBays(players[pid], color);
    if (pid === playerId) {
      drawThrust(x, y, a || 0, input?.move);
    }
  }

  drawBullets(bullets);
  ctx.restore();
  drawUIOverlay(view, state, input);
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
function drawUIOverlay(view) {
  ctx.save();
  ctx.translate(0, 0);

  if (view === "main_menu") {
    drawMainMenu();
  } else if (view === "editor") {
    // drawEditorUI();
  } else if (view === "shop") {
    // drawShopUI();
  } else console.warn("Unknown view:", view);

  ctx.restore();
}

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

function createSectorMap(count = 15, radius = 400, maxDist = 160) {
  const nodes = [];

  // Step 1: scatter non-overlapping nodes
  while (nodes.length < count) {
    const x = Math.random() * radius * 2 - radius;
    const y = Math.random() * radius * 2 - radius;
    if (nodes.every((n) => Math.hypot(n.x - x, n.y - y) > 50)) {
      nodes.push({ id: `n${nodes.length}`, x, y, links: [] });
    }
  }

  // Step 2: connect nearby nodes
  for (const a of nodes) {
    for (const b of nodes) {
      if (a === b) continue;
      const dist = Math.hypot(a.x - b.x, a.y - b.y);
      if (dist < maxDist && !a.links.includes(b.id)) {
        a.links.push(b.id);
        b.links.push(a.id);
      }
    }
  }

  return nodes;
}
function drawSectorMap(ctx, nodes) {
  ctx.save();
  ctx.translate(ctx.canvas.width / 2, ctx.canvas.height / 2);

  // Draw edges
  for (const n of nodes) {
    for (const id of n.links) {
      const t = nodes.find((n2) => n2.id === id);
      ctx.beginPath();
      ctx.moveTo(n.x, n.y);
      ctx.lineTo(t.x, t.y);
      ctx.strokeStyle = "#444";
      ctx.stroke();
    }
  }

  // Draw nodes
  for (const n of nodes) {
    ctx.beginPath();
    ctx.arc(n.x, n.y, 6, 0, Math.PI * 2);
    ctx.fillStyle = "#0ff";
    ctx.shadowColor = "#0ff";
    ctx.shadowBlur = 10;
    ctx.fill();
    ctx.strokeStyle = "#000";
    ctx.stroke();
  }

  ctx.restore();
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
