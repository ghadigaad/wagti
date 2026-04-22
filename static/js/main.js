/* ─── i18n ───────────────────────────────────────────────────────────────────── */
function I(key) {
  const x = window.__I18N__;
  return x && x[key] !== undefined ? x[key] : key;
}

function localeDigits(n) {
  if (document.documentElement.lang !== "ar") return String(n);
  const num = Number(n);
  return Number.isNaN(num) ? String(n) : num.toLocaleString("ar-SA", { maximumFractionDigits: 20 });
}

function pad2Time(n) {
  if (document.documentElement.lang !== "ar") return String(n).padStart(2, "0");
  return Number(n).toLocaleString("ar-SA", { minimumIntegerDigits: 2, maximumFractionDigits: 0, useGrouping: false });
}

function catLabel(c) {
  const m = { Study: I("cat_study"), Work: I("cat_work"), Personal: I("cat_personal") };
  return m[c] || c;
}

function statusLbl(s) {
  const m = { pending: I("status_pending"), active: I("status_active"), completed: I("status_completed") };
  return m[s] || s;
}

/* ─── State ──────────────────────────────────────────────────────────────────── */
let allTasks = [];
let tickInterval = null;

/* ─── Init ───────────────────────────────────────────────────────────────────── */
document.addEventListener("DOMContentLoaded", () => {
  loadTasks();
  document.getElementById("task-form").addEventListener("submit", handleAddTask);
  document.getElementById("filter-status").addEventListener("change", renderTasks);
  document.getElementById("filter-cat").addEventListener("change", renderTasks);

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
    toast(I("js_load_fail") + e.message, "error");
  }
}

/* ─── Add task ───────────────────────────────────────────────────────────────── */
async function handleAddTask(e) {
  e.preventDefault();
  const name = document.getElementById("task_name").value.trim();
  const category = document.getElementById("category").value;
  const expected_duration = parseInt(document.getElementById("expected_duration").value, 10) || 25;

  if (!name) return;

  try {
    const task = await api("/api/tasks", "POST", { task_name: name, category, expected_duration });
    allTasks.unshift(task);
    renderTasks();
    updateStats();
    document.getElementById("task-form").reset();
    document.getElementById("expected_duration").value = 25;
    toast(I("js_task_added"), "success");
  } catch (e) {
    toast(I("js_error_prefix") + e.message, "error");
  }
}

/* ─── Delete task ────────────────────────────────────────────────────────────── */
async function deleteTask(id) {
  if (!confirm(I("js_delete_confirm"))) return;
  try {
    await api(`/api/tasks/${id}`, "DELETE");
    allTasks = allTasks.filter(t => t.id !== id);
    renderTasks();
    updateStats();
    toast(I("js_task_deleted"), "info");
  } catch (e) {
    toast(I("js_error_prefix") + e.message, "error");
  }
}

/* ─── Start task ─────────────────────────────────────────────────────────────── */
async function startTask(id) {
  try {
    const updated = await api(`/api/tasks/${id}/start`, "POST");
    allTasks = allTasks.map(t => t.status === "active" ? { ...t, status: "pending" } : t);
    updateTask(updated);
    renderTasks();
    updateStats();
    toast(I("js_tracking_started"), "success");
  } catch (e) {
    toast(I("js_error_prefix") + e.message, "error");
  }
}

/* ─── Stop task ──────────────────────────────────────────────────────────────── */
async function stopTask(id) {
  try {
    const updated = await api(`/api/tasks/${id}/stop`, "POST");
    updateTask(updated);
    renderTasks();
    updateStats();
    toast(I("js_task_done"), "success");
  } catch (e) {
    toast(I("js_error_prefix") + e.message, "error");
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

  const tasks = allTasks.filter(t => {
    const matchStatus = filterStatus === "all" || t.status === filterStatus;
    const matchCat = filterCat === "all" || t.category === filterCat;
    return matchStatus && matchCat;
  });

  const container = document.getElementById("task-list");

  if (tasks.length === 0) {
    container.innerHTML = `
      <div class="empty-state">
        <i class="fa-regular fa-clipboard"></i>
        <p>${allTasks.length === 0 ? I("tasks_empty") : I("js_no_match_filters")}</p>
      </div>`;
    return;
  }

  container.innerHTML = tasks.map(t => taskHTML(t)).join("");
}

function taskHTML(t) {
  const catEmoji = { Study: "📚", Work: "💼", Personal: "🧘" }[t.category] || "";
  const catClass = `badge-${t.category.toLowerCase()}`;
  const statusClass = `badge-${t.status}`;
  const cLab = catLabel(t.category);
  const sLab = statusLbl(t.status);

  const elapsed = formatDuration(t.duration || 0);

  const expectedSec = (t.expected_duration || 25) * 60;
  const progress = t.duration ? Math.min(100, Math.round((t.duration / expectedSec) * 100)) : 0;

  const actionBtns = t.status === "pending"
    ? `<button class="btn btn-teal btn-sm" onclick="startTask(${t.id})"><i class="fa-solid fa-play"></i> ${I("js_start")}</button>`
    : t.status === "active"
    ? `<button class="btn btn-danger btn-sm" onclick="stopTask(${t.id})"><i class="fa-solid fa-stop"></i> ${I("js_stop")}</button>`
    : `<span class="badge badge-completed"><i class="fa-solid fa-check"></i> ${I("js_done")}</span>`;

  const suf = I("js_min_suffix");

  return `
    <div class="task-item ${t.status}" data-id="${t.id}">
      <div class="task-info">
        <div class="task-name">${escapeHTML(t.task_name)}</div>
        <div class="task-meta">
          <span class="badge ${catClass}">${catEmoji} ${cLab}</span>
          <span class="badge ${statusClass}">${sLab}</span>
          <span><i class="fa-regular fa-clock"></i> <span class="task-elapsed">${elapsed}</span> / ${localeDigits(t.expected_duration)}${suf}</span>
        </div>
        <div class="progress-bar" style="margin-top:8px;">
          <div class="progress-fill" style="width:${progress}%;"></div>
        </div>
      </div>
      <div class="task-actions">
        ${actionBtns}
        <button class="btn btn-ghost btn-sm btn-icon" onclick="deleteTask(${t.id})" title="${I("js_delete_title")}">
          <i class="fa-solid fa-trash"></i>
        </button>
      </div>
    </div>`;
}

/* ─── Stats ──────────────────────────────────────────────────────────────────── */
function saudiDateString(date) {
  const saudi = new Date(date.getTime() + 3 * 60 * 60 * 1000);
  return saudi.toISOString().slice(0, 10);
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

  document.getElementById("stat-active").textContent = localeDigits(active);
  document.getElementById("stat-completed").textContent = localeDigits(completed);
  document.getElementById("stat-time").textContent = formatDuration(totalSec, true);
}

/* ─── Utilities ──────────────────────────────────────────────────────────────── */
function formatDuration(seconds, short = false) {
  const zmin = I("dash_fmt_min");
  const suf = I("js_min_suffix");
  const jm = I("js_min");
  if (!seconds || seconds < 0) {
    return short ? zmin : (document.documentElement.lang === "ar" ? `${pad2Time(0)}:${pad2Time(0)}` : "0:00");
  }
  const h = Math.floor(seconds / 3600);
  const m = Math.floor((seconds % 3600) / 60);
  const s = seconds % 60;
  const fh = I("dash_fmt_h");
  if (short) {
    if (h > 0) return `${localeDigits(h)}${fh} ${localeDigits(m)}${jm}`;
    return `${localeDigits(m)}${suf}`;
  }
  if (h > 0) return `${localeDigits(h)}:${pad2Time(m)}:${pad2Time(s)}`;
  return `${localeDigits(m)}:${pad2Time(s)}`;
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
