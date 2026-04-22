/* ─── State ──────────────────────────────────────────────────────────────────── */
let allTasks = [];
let tickInterval = null;

/* ─── Init ───────────────────────────────────────────────────────────────────── */
document.addEventListener("DOMContentLoaded", () => {
  loadTasks();
  document.getElementById("task-form").addEventListener("submit", handleAddTask);
  document.getElementById("filter-status").addEventListener("change", renderTasks);
  document.getElementById("filter-cat").addEventListener("change", renderTasks);

  // Live elapsed time ticker
  tickInterval = setInterval(tick, 1000);
});

/* ─── API helpers ────────────────────────────────────────────────────────────── */
async function api(path, method = "GET", body = null) {
  const opts = { method, headers: { "Content-Type": "application/json" } };
  if (body) opts.body = JSON.stringify(body);
  const res = await fetch(path, opts);
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.error || `HTTP ${res.status}`);
  }
  return res.json();
}

/* ─── Load tasks ─────────────────────────────────────────────────────────────── */
async function loadTasks() {
  try {
    allTasks = await api("/api/tasks");
    renderTasks();
    updateStats();
  } catch (e) {
    toast("Failed to load tasks: " + e.message, "error");
  }
}

/* ─── Add task ───────────────────────────────────────────────────────────────── */
async function handleAddTask(e) {
  e.preventDefault();
  const name = document.getElementById("task_name").value.trim();
  const category = document.getElementById("category").value;
  const expected_duration = parseInt(document.getElementById("expected_duration").value) || 25;

  if (!name) return;

  try {
    const task = await api("/api/tasks", "POST", { task_name: name, category, expected_duration });
    allTasks.unshift(task);
    renderTasks();
    updateStats();
    document.getElementById("task-form").reset();
    document.getElementById("expected_duration").value = 25;
    toast("Task added!", "success");
  } catch (e) {
    toast("Error: " + e.message, "error");
  }
}

/* ─── Delete task ────────────────────────────────────────────────────────────── */
async function deleteTask(id) {
  if (!confirm("Delete this task?")) return;
  try {
    await api(`/api/tasks/${id}`, "DELETE");
    allTasks = allTasks.filter(t => t.id !== id);
    renderTasks();
    updateStats();
    toast("Task deleted", "info");
  } catch (e) {
    toast("Error: " + e.message, "error");
  }
}

/* ─── Start task ─────────────────────────────────────────────────────────────── */
async function startTask(id) {
  try {
    const updated = await api(`/api/tasks/${id}/start`, "POST");
    // Mark previously active as pending in local state
    allTasks = allTasks.map(t => t.status === "active" ? { ...t, status: "pending" } : t);
    updateTask(updated);
    renderTasks();
    updateStats();
    toast("Tracking started!", "success");
  } catch (e) {
    toast("Error: " + e.message, "error");
  }
}

/* ─── Stop task ──────────────────────────────────────────────────────────────── */
async function stopTask(id) {
  try {
    const updated = await api(`/api/tasks/${id}/stop`, "POST");
    updateTask(updated);
    renderTasks();
    updateStats();
    toast("Task completed! Great work.", "success");
  } catch (e) {
    toast("Error: " + e.message, "error");
  }
}

function updateTask(updated) {
  const idx = allTasks.findIndex(t => t.id === updated.id);
  if (idx !== -1) allTasks[idx] = updated;
}

/* ─── Live tick for active task ──────────────────────────────────────────────── */
function tick() {
  const active = allTasks.find(t => t.status === "active");
  if (!active || !active.start_time) return;

  const started = new Date(active.start_time + "Z");
  const elapsed = Math.floor((Date.now() - started.getTime()) / 1000) + (active.duration || 0);
  const el = document.querySelector(`[data-id="${active.id}"] .task-elapsed`);
  if (el) el.textContent = formatDuration(elapsed);
}

/* ─── Render ─────────────────────────────────────────────────────────────────── */
function renderTasks() {
  const filterStatus = document.getElementById("filter-status").value;
  const filterCat = document.getElementById("filter-cat").value;

  let tasks = allTasks.filter(t => {
    const matchStatus = filterStatus === "all" || t.status === filterStatus;
    const matchCat = filterCat === "all" || t.category === filterCat;
    return matchStatus && matchCat;
  });

  const container = document.getElementById("task-list");

  if (tasks.length === 0) {
    container.innerHTML = `
      <div class="empty-state">
        <i class="fa-regular fa-clipboard"></i>
        <p>No tasks match your filters.</p>
      </div>`;
    return;
  }

  container.innerHTML = tasks.map(t => taskHTML(t)).join("");
}

function taskHTML(t) {
  const catEmoji = { Study: "📚", Work: "💼", Personal: "🧘" }[t.category] || "";
  const catClass = `badge-${t.category.toLowerCase()}`;
  const statusClass = `badge-${t.status}`;

  const elapsed = t.status === "active"
    ? formatDuration((t.duration || 0))
    : formatDuration(t.duration || 0);

  const expectedSec = (t.expected_duration || 25) * 60;
  const progress = t.duration ? Math.min(100, Math.round((t.duration / expectedSec) * 100)) : 0;

  const actionBtns = t.status === "pending"
    ? `<button class="btn btn-teal btn-sm" onclick="startTask(${t.id})"><i class="fa-solid fa-play"></i> Start</button>`
    : t.status === "active"
    ? `<button class="btn btn-danger btn-sm" onclick="stopTask(${t.id})"><i class="fa-solid fa-stop"></i> Stop</button>`
    : `<span class="badge badge-completed"><i class="fa-solid fa-check"></i> Done</span>`;

  return `
    <div class="task-item ${t.status}" data-id="${t.id}">
      <div class="task-info">
        <div class="task-name">${escapeHTML(t.task_name)}</div>
        <div class="task-meta">
          <span class="badge ${catClass}">${catEmoji} ${t.category}</span>
          <span class="badge ${statusClass}">${t.status}</span>
          <span><i class="fa-regular fa-clock"></i> <span class="task-elapsed">${elapsed}</span> / ${t.expected_duration} min</span>
        </div>
        <div class="progress-bar" style="margin-top:8px;">
          <div class="progress-fill" style="width:${progress}%;"></div>
        </div>
      </div>
      <div class="task-actions">
        ${actionBtns}
        <button class="btn btn-ghost btn-sm btn-icon" onclick="deleteTask(${t.id})" title="Delete">
          <i class="fa-solid fa-trash"></i>
        </button>
      </div>
    </div>`;
}

/* ─── Stats ──────────────────────────────────────────────────────────────────── */
function saudiDateString(date) {
  // UTC+3 offset
  const saudi = new Date(date.getTime() + 3 * 60 * 60 * 1000);
  return saudi.toISOString().slice(0, 10); // "YYYY-MM-DD"
}

function updateStats() {
  const active = allTasks.filter(t => t.status === "active").length;
  const todayStr = saudiDateString(new Date());

  const todayTasks = allTasks.filter(t => {
    if (!t.start_time) return false;
    return saudiDateString(new Date(t.start_time + "Z")) === todayStr;
  });

  const completed = todayTasks.filter(t => t.status === "completed").length;
  const totalSec = todayTasks.reduce((s, t) => s + (t.duration || 0), 0);

  document.getElementById("stat-active").textContent = active;
  document.getElementById("stat-completed").textContent = completed;
  document.getElementById("stat-time").textContent = formatDuration(totalSec, true);
}

/* ─── Utilities ──────────────────────────────────────────────────────────────── */
function formatDuration(seconds, short = false) {
  if (!seconds || seconds < 0) return short ? "0 min" : "0:00";
  const h = Math.floor(seconds / 3600);
  const m = Math.floor((seconds % 3600) / 60);
  const s = seconds % 60;
  if (short) {
    if (h > 0) return `${h}h ${m}m`;
    return `${m} min`;
  }
  if (h > 0) return `${h}:${String(m).padStart(2, "0")}:${String(s).padStart(2, "0")}`;
  return `${m}:${String(s).padStart(2, "0")}`;
}

function escapeHTML(str) {
  return String(str).replace(/[&<>"']/g, c => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;"
  }[c]));
}

function toast(message, type = "info") {
  const container = document.getElementById("toast-container");
  const el = document.createElement("div");
  el.className = `toast toast-${type}`;
  const icons = { success: "fa-circle-check", error: "fa-circle-xmark", info: "fa-circle-info" };
  el.innerHTML = `<i class="fa-solid ${icons[type] || "fa-circle-info"}"></i> ${message}`;
  container.appendChild(el);
  setTimeout(() => el.remove(), 3500);
}
