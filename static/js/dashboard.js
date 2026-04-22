/* ─── Chart.js global defaults ───────────────────────────────────────────────── */
Chart.defaults.color = "#94a3b8";
Chart.defaults.font.family = "'Inter', system-ui, sans-serif";
Chart.defaults.font.size = 12;

const COLORS = {
  primary: "#ec4899",
  teal:    "#c084fc",
  accent:  "#f59e0b",
  success: "#22c55e",
  danger:  "#ef4444",
  info:    "#f472b6",
  muted:   "#64748b",
};

const CATEGORY_COLORS = {
  Study:    COLORS.info,
  Work:     COLORS.accent,
  Personal: COLORS.teal,
};

/* ─── Init ───────────────────────────────────────────────────────────────────── */
document.addEventListener("DOMContentLoaded", async () => {
  await Promise.all([
    loadDashboard(),
    loadScore(),
    loadWarnings(),
    loadRecommendations(),
  ]);
});

/* ─── Dashboard data ─────────────────────────────────────────────────────────── */
async function loadDashboard() {
  try {
    const data = await fetch("/api/dashboard").then(r => r.json());
    populateSummary(data.summary);
    renderDailyChart(data.daily);
    renderCategoryChart(data.category);
    renderHourlyChart(data.hourly);
  } catch (e) {
    console.error("Dashboard load failed:", e);
  }
}

/* ─── Summary cards ──────────────────────────────────────────────────────────── */
function populateSummary(s) {
  const m = s.total_today_min;
  document.getElementById("s-today").textContent =
    m >= 60 ? `${(m / 60).toFixed(1)}h` : m > 0 ? `${m} min` : "0 min";
  document.getElementById("s-tasks").textContent   = s.total_tasks_today;
  document.getElementById("s-alltime").textContent = `${s.total_all_time_hrs}h`;
}

function fmtMin(v) {
  if (v === 0) return "0 min";
  if (v < 1)  return `${Math.round(v * 60)}s`;
  return `${v} min`;
}

/* ─── Productivity Score ─────────────────────────────────────────────────────── */
async function loadScore() {
  try {
    const s = await fetch("/api/score").then(r => r.json());
    renderScore(s);
  } catch (e) {
    console.error("Score load failed:", e);
  }
}

function renderScore(s) {
  const score = s.score || 0;

  // Animate number
  const numEl = document.getElementById("s-score");
  let current = 0;
  const step = Math.ceil(score / 40);
  const timer = setInterval(() => {
    current = Math.min(current + step, score);
    numEl.textContent = current;
    if (current >= score) clearInterval(timer);
  }, 30);

  // SVG arc (circumference = 2π×18 ≈ 113.1)
  const arc  = document.getElementById("score-arc");
  const circ = 113.1;
  const offset = circ - (score / 100) * circ;
  setTimeout(() => {
    arc.style.strokeDashoffset = offset;
  }, 100);

  // Label & color
  const labelEl = document.getElementById("s-score-label");
  labelEl.textContent = s.label || "—";

  const color =
    score >= 80 ? "#22c55e" :
    score >= 60 ? "#ec4899" :
    score >= 40 ? "#f59e0b" : "#ef4444";
  arc.style.stroke = color;
  labelEl.style.color = color;

  // Breakdown bars
  const bd = s.breakdown || {};
  setBreakdown("focus", bd.focus || 0, 40);
  setBreakdown("tasks", bd.tasks || 0, 30);
  setBreakdown("cons",  bd.consistency || 0, 30);

  document.getElementById("score-breakdown-card").style.display = "block";
}

function setBreakdown(key, pts, max) {
  const pct = Math.round((pts / max) * 100);
  document.getElementById(`br-${key}`).style.width = `${pct}%`;
  document.getElementById(`br-${key}-pts`).textContent = `${pts} / ${max} pts`;
}

/* ─── Smart Warnings ─────────────────────────────────────────────────────────── */
async function loadWarnings() {
  try {
    const warnings = await fetch("/api/warnings").then(r => r.json());
    renderWarnings(warnings);
  } catch (e) {
    console.error("Warnings load failed:", e);
  }
}

function renderWarnings(warnings) {
  if (!warnings || !warnings.length) return;

  const card = document.getElementById("warnings-card");
  const list = document.getElementById("warnings-list");
  card.style.display = "block";

  list.innerHTML = warnings.map(w => `
    <div class="warning-item ${w.type}">
      <div class="warning-icon ${w.type}">
        <i class="fa-solid ${w.icon}"></i>
      </div>
      <div style="font-size:0.88rem; color:var(--text);">${w.text}</div>
    </div>
  `).join("");
}

/* ─── Recommendations + Prediction ──────────────────────────────────────────── */
async function loadRecommendations() {
  try {
    const result = await fetch("/api/recommendations").then(r => r.json());
    renderRecommendations(result.tips || []);
    renderPrediction(result.prediction || null);
  } catch (e) {
    document.getElementById("rec-list").innerHTML =
      `<div class="empty-state"><i class="fa-solid fa-circle-exclamation"></i><p>Could not load recommendations.</p></div>`;
  }
}

function renderRecommendations(tips) {
  const container = document.getElementById("rec-list");
  if (!tips.length) {
    container.innerHTML = `<div class="empty-state"><i class="fa-solid fa-lightbulb"></i><p>Complete more tasks to unlock insights.</p></div>`;
    return;
  }

  container.innerHTML = tips.map(tip => `
    <div class="rec-item">
      <div class="rec-icon ${tip.type}">
        <i class="fa-solid ${tip.icon}"></i>
      </div>
      <div class="rec-content">
        <div class="rec-title">${tip.title}</div>
        <div class="rec-text">${tip.text}</div>
      </div>
    </div>
  `).join("");
}

function renderPrediction(pred) {
  if (!pred) return;

  const card = document.getElementById("prediction-card");
  card.style.display = "block";

  document.getElementById("pred-title").textContent =
    `Tomorrow (${pred.day_name}): Best focus at ${pred.range_label}`;
  document.getElementById("pred-sub").textContent =
    `Based on your historical patterns, you are most productive during this window on ${pred.day_name}s.`;
  document.getElementById("pred-confidence").innerHTML =
    `<i class="fa-solid fa-signal"></i> Confidence: ${pred.confidence} &nbsp;·&nbsp; ${pred.sessions} past sessions`;
}

/* ─── Daily Bar Chart ────────────────────────────────────────────────────────── */
function renderDailyChart(data) {
  const ctx = document.getElementById("chart-daily").getContext("2d");
  new Chart(ctx, {
    type: "bar",
    data: {
      labels: data.labels,
      datasets: [{
        label: "Minutes",
        data:  data.values,
        backgroundColor: data.values.map((_, i) =>
          i === data.values.length - 1 ? COLORS.primary : "rgba(236,72,153,0.3)"
        ),
        borderColor:  COLORS.primary,
        borderWidth:  1.5,
        borderRadius: 6,
      }],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: { callbacks: { label: ctx => fmtMin(ctx.parsed.y) } },
      },
      scales: {
        x: { grid: { color: "rgba(255,255,255,0.05)" } },
        y: {
          grid:       { color: "rgba(255,255,255,0.05)" },
          ticks:      { callback: v => fmtMin(v) },
          beginAtZero: true,
        },
      },
    },
  });
}

/* ─── Category Doughnut Chart ────────────────────────────────────────────────── */
function renderCategoryChart(data) {
  const ctx = document.getElementById("chart-category").getContext("2d");

  if (!data.labels.length) {
    ctx.canvas.parentElement.innerHTML =
      `<div class="empty-state" style="padding:2rem;"><i class="fa-solid fa-chart-pie"></i><p>No data for today yet.</p></div>`;
    return;
  }

  const bgColors = data.labels.map(l => CATEGORY_COLORS[l] || COLORS.muted);
  new Chart(ctx, {
    type: "doughnut",
    data: {
      labels: data.labels,
      datasets: [{
        data:            data.values,
        backgroundColor: bgColors,
        borderColor:     "#1a0b2e",
        borderWidth:     3,
        hoverOffset:     8,
      }],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      cutout: "68%",
      plugins: {
        legend: {
          position: "bottom",
          labels:   { padding: 16, usePointStyle: true, pointStyleWidth: 10 },
        },
        tooltip: { callbacks: { label: ctx => ` ${ctx.label}: ${fmtMin(ctx.parsed)}` } },
      },
    },
  });
}

/* ─── Hourly Line Chart ──────────────────────────────────────────────────────── */
function renderHourlyChart(data) {
  const ctx = document.getElementById("chart-hourly").getContext("2d");

  const gradient = ctx.createLinearGradient(0, 0, 0, 300);
  gradient.addColorStop(0, "rgba(236, 72, 153, 0.35)");
  gradient.addColorStop(1, "rgba(236, 72, 153, 0)");

  new Chart(ctx, {
    type: "line",
    data: {
      labels: data.labels,
      datasets: [{
        label:              "Minutes",
        data:               data.values,
        borderColor:        COLORS.primary,
        backgroundColor:    gradient,
        fill:               true,
        tension:            0.4,
        pointRadius:        data.values.map(v => v > 0 ? 4 : 0),
        pointBackgroundColor: COLORS.primary,
        borderWidth:        2,
      }],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: { callbacks: { label: ctx => fmtMin(ctx.parsed.y) } },
      },
      scales: {
        x: {
          grid:  { color: "rgba(255,255,255,0.05)" },
          ticks: { maxTicksLimit: 12, callback: (val, idx) => data.labels[idx] },
        },
        y: {
          grid:        { color: "rgba(255,255,255,0.05)" },
          ticks:       { callback: v => fmtMin(v) },
          beginAtZero: true,
        },
      },
    },
  });
}
