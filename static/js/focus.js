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

function makeModes() {
  return {
    pomodoro: { label: I("focus_label_focus"), duration: 25 * 60, color: "var(--primary)" },
    short: { label: I("focus_label_short"), duration: 5 * 60, color: "var(--teal)" },
    long: { label: I("focus_label_long"), duration: 15 * 60, color: "var(--teal)" },
  };
}

let MODES = {};

/* ─── State ──────────────────────────────────────────────────────────────────── */
let currentMode = "pomodoro";
let timeLeft = 25 * 60;
let totalDuration = 25 * 60;
let running = false;
let intervalId = null;
let pomodorosCompleted = 0;
let pomodorosTodayCount = parseInt(localStorage.getItem("pom_today") || "0", 10);
let totalFocusSeconds = parseInt(localStorage.getItem("pom_focus_sec") || "0", 10);
let lastDate = localStorage.getItem("pom_date") || "";

const today = new Date().toDateString();
if (lastDate !== today) {
  pomodorosTodayCount = 0;
  totalFocusSeconds = 0;
  localStorage.setItem("pom_today", "0");
  localStorage.setItem("pom_focus_sec", "0");
  localStorage.setItem("pom_date", today);
}

const CIRCUMFERENCE = 2 * Math.PI * 114;

function docTitleBase() {
  return I("focus_doc_title");
}

document.addEventListener("DOMContentLoaded", () => {
  MODES = makeModes();
  timeLeft = MODES.pomodoro.duration;
  totalDuration = MODES.pomodoro.duration;

  updateDisplay();
  updateRing();
  updateDots();
  updateSessionStats();
  requestNotificationPermission();

  document.addEventListener("visibilitychange", () => {
    if (document.hidden && running && currentMode === "pomodoro") {
      showAlert(true);
      flashTitle(I("focus_title_flash"));
    } else {
      showAlert(false);
      document.title = docTitleBase();
    }
  });
});

function setMode(mode) {
  MODES = makeModes();
  if (running) resetTimer();
  currentMode = mode;
  timeLeft = MODES[mode].duration;
  totalDuration = MODES[mode].duration;

  document.getElementById("btn-pomodoro").className = "timer-mode-btn" + (mode === "pomodoro" ? " active" : "");
  document.getElementById("btn-short").className = "timer-mode-btn break" + (mode === "short" ? " active" : "");
  document.getElementById("btn-long").className = "timer-mode-btn break" + (mode === "long" ? " active" : "");

  const ring = document.getElementById("ring-progress");
  ring.className = "timer-ring-progress" + (mode !== "pomodoro" ? " break" : "");

  updateDisplay();
  updateRing();
  document.getElementById("stat-mode").textContent = MODES[mode].label;
  showAlert(false);
}

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
  document.getElementById("btn-start").innerHTML =
    `<i class="fa-solid fa-play"></i> ${I("focus_resume")}`;
}

function resetTimer() {
  MODES = makeModes();
  running = false;
  clearInterval(intervalId);
  timeLeft = MODES[currentMode].duration;
  document.getElementById("btn-start").style.display = "inline-flex";
  document.getElementById("btn-pause").style.display = "none";
  document.getElementById("btn-start").innerHTML =
    `<i class="fa-solid fa-play"></i> ${I("focus_start")}`;
  updateDisplay();
  updateRing();
  showAlert(false);
}

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

function onTimerComplete() {
  MODES = makeModes();
  document.getElementById("btn-start").style.display = "inline-flex";
  document.getElementById("btn-pause").style.display = "none";
  document.getElementById("btn-start").innerHTML =
    `<i class="fa-solid fa-play"></i> ${I("focus_start")}`;

  if (currentMode === "pomodoro") {
    pomodorosCompleted++;
    pomodorosTodayCount++;
    localStorage.setItem("pom_today", pomodorosTodayCount);
    localStorage.setItem("pom_date", today);
    updateDots();
    updateSessionStats();

    notify(I("focus_notify_pomo_title"), I("focus_notify_pomo_body"));
    toast(I("focus_toast_pomo_done"), "success");

    if (pomodorosCompleted % 4 === 0) {
      setTimeout(() => setMode("long"), 1000);
    } else {
      setTimeout(() => setMode("short"), 1000);
    }
  } else {
    notify(I("focus_notify_break_title"), I("focus_notify_break_body"));
    toast(I("focus_toast_break_done"), "info");
    setTimeout(() => setMode("pomodoro"), 1000);
  }
}

function updateDisplay() {
  const m = Math.floor(timeLeft / 60);
  const s = timeLeft % 60;
  const text = `${pad2Time(m)}:${pad2Time(s)}`;
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

function updateDots() {
  for (let i = 0; i < 4; i++) {
    const dot = document.getElementById(`dot-${i}`);
    dot.className = "pom-dot" + (i < (pomodorosCompleted % 4 || (pomodorosCompleted > 0 && pomodorosCompleted % 4 === 0 ? 4 : 0)) ? " done" : "");
  }
}

function updateSessionStats() {
  document.getElementById("stat-pom-today").textContent = localeDigits(pomodorosTodayCount);
  const mins = Math.floor(totalFocusSeconds / 60);
  const suf = I("js_min_suffix");
  document.getElementById("stat-focus-time").textContent =
    mins > 0 ? `${localeDigits(mins)}${suf}` : `${localeDigits(0)}${suf}`;
}

function showAlert(show) {
  document.getElementById("focus-alert").style.display = show ? "flex" : "none";
}

let titleFlashInterval = null;
function flashTitle(msg) {
  let toggle = true;
  clearInterval(titleFlashInterval);
  titleFlashInterval = setInterval(() => {
    document.title = toggle ? msg : docTitleBase();
    toggle = !toggle;
  }, 1000);

  document.addEventListener("visibilitychange", () => {
    if (!document.hidden) {
      clearInterval(titleFlashInterval);
      titleFlashInterval = null;
    }
  }, { once: true });
}

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

function toast(message, type = "info") {
  const container = document.getElementById("toast-container");
  const el = document.createElement("div");
  el.className = `toast toast-${type}`;
  const icons = { success: "fa-circle-check", error: "fa-circle-xmark", info: "fa-circle-info" };
  el.innerHTML = `<i class="fa-solid ${icons[type] || "fa-circle-info"}"></i> ${message}`;
  container.appendChild(el);
  setTimeout(() => el.remove(), 4000);
}
