/* ─── Modes ──────────────────────────────────────────────────────────────────── */
const MODES = {
  pomodoro: { label: "Focus", duration: 25 * 60, color: "var(--primary)" },
  short: { label: "Short Break", duration: 5 * 60, color: "var(--teal)" },
  long: { label: "Long Break", duration: 15 * 60, color: "var(--teal)" },
};

/* ─── State ──────────────────────────────────────────────────────────────────── */
let currentMode = "pomodoro";
let timeLeft = MODES.pomodoro.duration;
let totalDuration = MODES.pomodoro.duration;
let running = false;
let intervalId = null;
let pomodorosCompleted = 0;  // session
let pomodorosTodayCount = parseInt(localStorage.getItem("pom_today") || "0");
let totalFocusSeconds = parseInt(localStorage.getItem("pom_focus_sec") || "0");
let lastDate = localStorage.getItem("pom_date") || "";

// Reset daily stats if new day
const today = new Date().toDateString();
if (lastDate !== today) {
  pomodorosTodayCount = 0;
  totalFocusSeconds = 0;
  localStorage.setItem("pom_today", "0");
  localStorage.setItem("pom_focus_sec", "0");
  localStorage.setItem("pom_date", today);
}

const CIRCUMFERENCE = 2 * Math.PI * 114; // r=114

/* ─── Init ───────────────────────────────────────────────────────────────────── */
document.addEventListener("DOMContentLoaded", () => {
  updateDisplay();
  updateRing();
  updateDots();
  updateSessionStats();
  requestNotificationPermission();

  // Page Visibility API — alert when user switches tabs during focus
  document.addEventListener("visibilitychange", () => {
    if (document.hidden && running && currentMode === "pomodoro") {
      showAlert(true);
      flashTitle("⚠️ Stay Focused!");
    } else {
      showAlert(false);
      document.title = "Deep Focus — Wagti";
    }
  });
});

/* ─── Mode selection ─────────────────────────────────────────────────────────── */
function setMode(mode) {
  if (running) resetTimer();
  currentMode = mode;
  timeLeft = MODES[mode].duration;
  totalDuration = MODES[mode].duration;

  // Update button styles
  document.getElementById("btn-pomodoro").className = "timer-mode-btn" + (mode === "pomodoro" ? " active" : "");
  document.getElementById("btn-short").className = "timer-mode-btn break" + (mode === "short" ? " active" : "");
  document.getElementById("btn-long").className = "timer-mode-btn break" + (mode === "long" ? " active" : "");

  // Ring color
  const ring = document.getElementById("ring-progress");
  ring.className = "timer-ring-progress" + (mode !== "pomodoro" ? " break" : "");

  updateDisplay();
  updateRing();
  document.getElementById("stat-mode").textContent = MODES[mode].label;
  showAlert(false);
}

/* ─── Timer controls ─────────────────────────────────────────────────────────── */
function startTimer() {
  if (running) return;
  running = true;
  document.getElementById("btn-start").style.display = "none";
  document.getElementById("btn-pause").style.display = "inline-flex";

  intervalId = setInterval(tick, 1000);
}

function pauseTimer() {
  running = false;
  clearInterval(intervalId);
  document.getElementById("btn-start").style.display = "inline-flex";
  document.getElementById("btn-pause").style.display = "none";
  document.getElementById("btn-start").innerHTML = '<i class="fa-solid fa-play"></i> Resume';
}

function resetTimer() {
  running = false;
  clearInterval(intervalId);
  timeLeft = MODES[currentMode].duration;
  document.getElementById("btn-start").style.display = "inline-flex";
  document.getElementById("btn-pause").style.display = "none";
  document.getElementById("btn-start").innerHTML = '<i class="fa-solid fa-play"></i> Start';
  updateDisplay();
  updateRing();
  showAlert(false);
}

/* ─── Tick ───────────────────────────────────────────────────────────────────── */
function tick() {
  if (timeLeft <= 0) {
    clearInterval(intervalId);
    running = false;
    onTimerComplete();
    return;
  }

  if (currentMode === "pomodoro") {
    totalFocusSeconds++;
    localStorage.setItem("pom_focus_sec", totalFocusSeconds);
  }

  timeLeft--;
  updateDisplay();
  updateRing();
}

/* ─── Timer complete ─────────────────────────────────────────────────────────── */
function onTimerComplete() {
  document.getElementById("btn-start").style.display = "inline-flex";
  document.getElementById("btn-pause").style.display = "none";
  document.getElementById("btn-start").innerHTML = '<i class="fa-solid fa-play"></i> Start';

  if (currentMode === "pomodoro") {
    pomodorosCompleted++;
    pomodorosTodayCount++;
    localStorage.setItem("pom_today", pomodorosTodayCount);
    localStorage.setItem("pom_date", today);
    updateDots();
    updateSessionStats();

    notify("Pomodoro Complete! 🎉", "Great work! Time for a break.");
    toast("Pomodoro done! Take a break.", "success");

    // Auto-suggest break after 4 pomodoros
    if (pomodorosCompleted % 4 === 0) {
      setTimeout(() => setMode("long"), 1000);
    } else {
      setTimeout(() => setMode("short"), 1000);
    }
  } else {
    notify("Break Over!", "Time to focus again.");
    toast("Break finished. Let's get back to work!", "info");
    setTimeout(() => setMode("pomodoro"), 1000);
  }
}

/* ─── Display ────────────────────────────────────────────────────────────────── */
function updateDisplay() {
  const m = Math.floor(timeLeft / 60);
  const s = timeLeft % 60;
  const text = `${String(m).padStart(2, "0")}:${String(s).padStart(2, "0")}`;
  document.getElementById("timer-display").textContent = text;
  document.getElementById("timer-label").textContent = MODES[currentMode].label;
  document.title = `${text} — Wagti`;
}

function updateRing() {
  const progress = timeLeft / totalDuration;
  const offset = CIRCUMFERENCE * (1 - progress);
  document.getElementById("ring-progress").style.strokeDasharray = CIRCUMFERENCE;
  document.getElementById("ring-progress").style.strokeDashoffset = offset;
}

/* ─── Pomodoro dots ──────────────────────────────────────────────────────────── */
function updateDots() {
  for (let i = 0; i < 4; i++) {
    const dot = document.getElementById(`dot-${i}`);
    dot.className = "pom-dot" + (i < (pomodorosCompleted % 4 || (pomodorosCompleted > 0 && pomodorosCompleted % 4 === 0 ? 4 : 0)) ? " done" : "");
  }
}

/* ─── Session stats ──────────────────────────────────────────────────────────── */
function updateSessionStats() {
  document.getElementById("stat-pom-today").textContent = pomodorosTodayCount;
  const mins = Math.floor(totalFocusSeconds / 60);
  document.getElementById("stat-focus-time").textContent = mins > 0 ? `${mins} min` : "0 min";
}

/* ─── Alert ──────────────────────────────────────────────────────────────────── */
function showAlert(show) {
  document.getElementById("focus-alert").style.display = show ? "flex" : "none";
}

let titleFlashInterval = null;
function flashTitle(msg) {
  let toggle = true;
  clearInterval(titleFlashInterval);
  titleFlashInterval = setInterval(() => {
    document.title = toggle ? msg : "Deep Focus — Wagti";
    toggle = !toggle;
  }, 1000);

  document.addEventListener("visibilitychange", () => {
    if (!document.hidden) {
      clearInterval(titleFlashInterval);
      titleFlashInterval = null;
    }
  }, { once: true });
}

/* ─── Notifications ──────────────────────────────────────────────────────────── */
function requestNotificationPermission() {
  if ("Notification" in window && Notification.permission === "default") {
    Notification.requestPermission();
  }
}

function notify(title, body) {
  if ("Notification" in window && Notification.permission === "granted") {
    new Notification(title, { body, icon: "/static/favicon.ico" });
  }
}

/* ─── Toast ──────────────────────────────────────────────────────────────────── */
function toast(message, type = "info") {
  const container = document.getElementById("toast-container");
  const el = document.createElement("div");
  el.className = `toast toast-${type}`;
  const icons = { success: "fa-circle-check", error: "fa-circle-xmark", info: "fa-circle-info" };
  el.innerHTML = `<i class="fa-solid ${icons[type] || "fa-circle-info"}"></i> ${message}`;
  container.appendChild(el);
  setTimeout(() => el.remove(), 4000);
}
