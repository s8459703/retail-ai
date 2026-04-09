"use strict";

// Apply saved theme immediately before DOM renders to avoid flash
(function() {
    const t = localStorage.getItem("retailai-theme") || "dark";
    document.documentElement.setAttribute("data-theme", t);
})();

/* ═══════════════════════════════════════════════════════════
   dashboard.js  —  Shared JS for Retail AI inner pages
   Covers: sidebar, upload, predict, settings
   ═══════════════════════════════════════════════════════════ */

/* ── Helpers ─────────────────────────────────────────────── */
const $ = (sel, ctx = document) => ctx.querySelector(sel);
const $$ = (sel, ctx = document) => [...ctx.querySelectorAll(sel)];

/* ── Run after DOM ready ─────────────────────────────────── */
document.addEventListener("DOMContentLoaded", () => {
    initCharts();
    initSidebar();
    initActiveNav();
    initUpload();
    initPredict();
    initSettings();
});

/* ══════════════════════════════════════════════════════════
   1. CHARTS — read data from canvas data-* attributes
   ══════════════════════════════════════════════════════════ */
function initCharts() {
    const PALETTE = [
        "#667eea", "#764ba2", "#f093fb", "#4facfe",
        "#43e97b", "#fa709a", "#fee140", "#30cfd0",
        "#a18cd1", "#fda085"
    ];
    const darkGrid   = "rgba(255,255,255,0.05)";
    const tickColor  = "#888";
    const legendOpts = { labels: { color: "rgba(255,255,255,0.75)", padding: 16 } };
    const dollarTick = (v) => "$" + v.toLocaleString();

    // Read data from <script type="application/json"> islands — safe, no attribute escaping
    function readIsland(id) {
        const el = document.getElementById(id);
        return el ? JSON.parse(el.textContent) : [];
    }

    const categories    = readIsland("data-categories");
    const categorySales = readIsland("data-category-sales");
    const monthlyLabels = readIsland("data-monthly-labels");
    const monthlySales  = readIsland("data-monthly-sales");

    // Bar chart — sales by category
    const barEl = document.getElementById("barChart");
    if (barEl && categories.length) {
        new Chart(barEl, {
            type: "bar",
            data: {
                labels: categories,
                datasets: [{
                    label: "Revenue ($)",
                    data: categorySales,
                    backgroundColor: "rgba(102,126,234,0.75)",
                    borderColor: "#667eea",
                    borderWidth: 1,
                    borderRadius: 6,
                }]
            },
            options: {
                responsive: true,
                plugins: { legend: legendOpts },
                scales: {
                    x: { ticks: { color: tickColor }, grid: { color: darkGrid } },
                    y: { ticks: { color: tickColor, callback: dollarTick }, grid: { color: darkGrid } }
                }
            }
        });
    }

    // Doughnut chart — category distribution
    const pieEl = document.getElementById("pieChart");
    if (pieEl && categories.length) {
        new Chart(pieEl, {
            type: "doughnut",
            data: {
                labels: categories,
                datasets: [{
                    data: categorySales,
                    backgroundColor: PALETTE,
                    borderWidth: 2,
                    borderColor: "rgba(15,15,35,0.8)"
                }]
            },
            options: {
                responsive: true,
                plugins: { legend: legendOpts }
            }
        });
    }

    // Line chart — monthly sales trend
    const lineEl = document.getElementById("lineChart");
    if (lineEl && monthlyLabels.length) {
        new Chart(lineEl, {
            type: "line",
            data: {
                labels: monthlyLabels,
                datasets: [{
                    label: "Monthly Revenue ($)",
                    data: monthlySales,
                    borderColor: "#667eea",
                    backgroundColor: "rgba(102,126,234,0.12)",
                    borderWidth: 2,
                    pointBackgroundColor: "#667eea",
                    pointRadius: 4,
                    tension: 0.4,
                    fill: true,
                }]
            },
            options: {
                responsive: true,
                plugins: { legend: legendOpts },
                scales: {
                    x: { ticks: { color: tickColor }, grid: { color: darkGrid } },
                    y: { ticks: { color: tickColor, callback: dollarTick }, grid: { color: darkGrid } }
                }
            }
        });
    }
}

/* ══════════════════════════════════════════════════════════
   2. SIDEBAR — toggle open/close on mobile
   ══════════════════════════════════════════════════════════ */
function initSidebar() {
    const sidebar = $("#sidebar");
    const overlay = $("#sidebarOverlay");
    const toggle  = $("#sidebarToggle");

    if (!sidebar || !toggle) return;

    toggle.addEventListener("click", () => {
        sidebar.classList.toggle("open");
        overlay?.classList.toggle("active");
    });

    overlay?.addEventListener("click", closeSidebar);
    document.addEventListener("keydown", (e) => { if (e.key === "Escape") closeSidebar(); });

    function closeSidebar() {
        sidebar.classList.remove("open");
        overlay?.classList.remove("active");
    }

    // Live date in topbar
    const dateEl = $("#topbarDate");
    if (dateEl) {
        const update = () => {
            dateEl.textContent = new Date().toLocaleDateString("en-US", {
                weekday: "short", year: "numeric", month: "short", day: "numeric"
            });
        };
        update();
        setInterval(update, 60_000);
    }
}

/* ══════════════════════════════════════════════════════════
   3. ACTIVE NAV — highlight current page link
   ══════════════════════════════════════════════════════════ */
function initActiveNav() {
    const currentPath = window.location.pathname;

    $$(".nav-item").forEach((link) => {
        const href = link.getAttribute("href") || "";
        // Match exact path or sub-path (e.g. /dashboard matches /dashboard)
        if (href && currentPath.startsWith(href) && href !== "/") {
            link.classList.add("active");
        } else if (href === "/" && currentPath === "/") {
            link.classList.add("active");
        } else {
            link.classList.remove("active");
        }
    });
}

/* ══════════════════════════════════════════════════════════
   4. UPLOAD PAGE — drag & drop, file validation, CSV preview
   ══════════════════════════════════════════════════════════ */
function initUpload() {
    const dropZone = $("#dropZone");
    const fileInput = $("#dataFile");
    const processBtn = $("#processBtn");
    const progressWrap = $("#progress");
    const progressFill = $(".progress-fill");
    const progressText = progressWrap ? progressWrap.querySelector("span") : null;
    const preview = $("#preview");
    const dataTable = $("#dataTable");

    if (!dropZone) return;

    // Click on drop zone opens file picker
    dropZone.addEventListener("click", () => fileInput?.click());

    // Drag events
    ["dragenter", "dragover"].forEach((evt) => {
        dropZone.addEventListener(evt, (e) => {
            e.preventDefault();
            dropZone.classList.add("drag-over");
        });
    });

    ["dragleave", "dragend", "drop"].forEach((evt) => {
        dropZone.addEventListener(evt, () => dropZone.classList.remove("drag-over"));
    });

    dropZone.addEventListener("drop", (e) => {
        e.preventDefault();
        const files = e.dataTransfer?.files;
        if (files?.length) handleFile(files[0]);
    });

    fileInput?.addEventListener("change", () => {
        if (fileInput.files?.length) handleFile(fileInput.files[0]);
    });

    processBtn?.addEventListener("click", () => {
        if (!fileInput?.files?.length) {
            showToast("Please select a CSV file first.", "error");
            return;
        }
        handleFile(fileInput.files[0]);
    });

    function handleFile(file) {
        if (!file.name.endsWith(".csv")) {
            showToast("Only CSV files are supported.", "error");
            return;
        }

        simulateProgress(progressWrap, progressFill, progressText, () => {
            const reader = new FileReader();
            reader.onload = (e) => {
                const rows = parseCSV(e.target.result);
                if (rows.length < 2) {
                    showToast("CSV appears to be empty.", "error");
                    return;
                }
                renderTable(dataTable, rows);
                if (preview) preview.style.display = "block";
                showToast(`Loaded ${rows.length - 1} rows from ${file.name}`, "success");
            };
            reader.readAsText(file);
        });
    }
}

/* Parse CSV text → array of arrays */
function parseCSV(text) {
    return text
        .trim()
        .split("\n")
        .map((line) => line.split(",").map((cell) => cell.trim().replace(/^"|"$/g, "")));
}

/* Render parsed CSV rows into a <table> element */
function renderTable(tableEl, rows) {
    if (!tableEl) return;
    const [headers, ...body] = rows;

    const thead = headers.map((h) => `<th>${escapeHtml(h)}</th>`).join("");
    const tbody = body
        .slice(0, 20) // preview first 20 rows
        .map((row) => `<tr>${row.map((c) => `<td>${escapeHtml(c)}</td>`).join("")}</tr>`)
        .join("");

    tableEl.innerHTML = `<thead><tr>${thead}</tr></thead><tbody>${tbody}</tbody>`;
}

/* Simulate a progress bar, then fire callback */
function simulateProgress(wrap, fill, text, onComplete) {
    if (!wrap || !fill) { onComplete(); return; }

    wrap.style.display = "block";
    let pct = 0;

    const interval = setInterval(() => {
        pct = Math.min(pct + Math.random() * 18, 95);
        fill.style.width = `${pct}%`;
        if (text) text.textContent = `${Math.round(pct)}%`;
    }, 120);

    setTimeout(() => {
        clearInterval(interval);
        fill.style.width = "100%";
        if (text) text.textContent = "100%";
        setTimeout(() => {
            wrap.style.display = "none";
            fill.style.width = "0%";
            onComplete();
        }, 400);
    }, 1400);
}

/* ══════════════════════════════════════════════════════════
   5. PREDICT PAGE — loading state on form submit
   ══════════════════════════════════════════════════════════ */
function initPredict() {
    const form = $("form[action*='predict'], form#predictForm");
    const submitBtn = form ? $("[type='submit']", form) : null;

    if (!form || !submitBtn) return;

    form.addEventListener("submit", () => {
        submitBtn.disabled = true;
        submitBtn.innerHTML = `<i class="fas fa-spinner fa-spin"></i> Generating…`;
    });
}

/* ══════════════════════════════════════════════════════════
   6. SETTINGS PAGE — theme switcher + toggle persistence
   ══════════════════════════════════════════════════════════ */
function initSettings() {
    initThemeSwitcher();
    initTogglePersistence();
}

function initThemeSwitcher() {
    const themeBtns = $$("[data-theme]");
    if (!themeBtns.length) return;

    const saved = localStorage.getItem("retailai-theme") || "dark";
    applyTheme(saved);
    themeBtns.forEach(btn => btn.classList.toggle("active", btn.dataset.theme === saved));

    themeBtns.forEach(btn => {
        btn.addEventListener("click", () => {
            const theme = btn.dataset.theme;
            applyTheme(theme);
            localStorage.setItem("retailai-theme", theme);
            themeBtns.forEach(b => b.classList.toggle("active", b === btn));
            showToast(`Theme changed to ${theme}.`, "info");
        });
    });
}

function applyTheme(theme) {
    document.documentElement.setAttribute("data-theme", theme);
}

function initTogglePersistence() {
    // Persist all named checkboxes inside [data-settings] form
    document.querySelectorAll("[data-settings] input[type='checkbox'][name]").forEach((checkbox) => {
        const key = `retailai-toggle-${checkbox.name}`;
        const saved = localStorage.getItem(key);
        if (saved !== null) checkbox.checked = saved === "true";

        checkbox.addEventListener("change", () => {
            localStorage.setItem(key, checkbox.checked);
            showToast(
                `${checkbox.name.replace(/-/g, " ")} ${checkbox.checked ? "enabled" : "disabled"}.`,
                "info"
            );
        });
    });

    // Settings save button feedback
    const saveBtn = document.querySelector("#saveSettingsBtn");
    if (saveBtn) {
        saveBtn.addEventListener("click", (e) => {
            e.preventDefault();
            const orig = saveBtn.innerHTML;
            saveBtn.innerHTML = `<i class="fas fa-check"></i> Saved!`;
            saveBtn.disabled = true;
            setTimeout(() => {
                saveBtn.innerHTML = orig;
                saveBtn.disabled = false;
            }, 2000);
        });
    }
}

/* ══════════════════════════════════════════════════════════
   7. TOAST NOTIFICATIONS
   ══════════════════════════════════════════════════════════ */
function showToast(message, type = "info") {
    let container = $("#toast-container");
    if (!container) {
        container = document.createElement("div");
        container.id = "toast-container";
        Object.assign(container.style, {
            position: "fixed",
            bottom: "1.5rem",
            right: "1.5rem",
            display: "flex",
            flexDirection: "column",
            gap: "0.5rem",
            zIndex: "9999",
        });
        document.body.appendChild(container);
    }

    const colors = {
        success: { bg: "rgba(34,197,94,0.15)", border: "rgba(34,197,94,0.4)", text: "#86efac" },
        error: { bg: "rgba(239,68,68,0.15)", border: "rgba(239,68,68,0.4)", text: "#fca5a5" },
        info: { bg: "rgba(102,126,234,0.15)", border: "rgba(102,126,234,0.4)", text: "#a5b4fc" },
    };
    const c = colors[type] || colors.info;

    const toast = document.createElement("div");
    Object.assign(toast.style, {
        background: c.bg,
        border: `1px solid ${c.border}`,
        color: c.text,
        padding: "0.75rem 1.25rem",
        borderRadius: "10px",
        fontSize: "0.875rem",
        fontFamily: "'Segoe UI', sans-serif",
        backdropFilter: "blur(10px)",
        boxShadow: "0 4px 20px rgba(0,0,0,0.3)",
        opacity: "0",
        transform: "translateY(8px)",
        transition: "opacity 0.25s ease, transform 0.25s ease",
        maxWidth: "320px",
    });
    toast.textContent = message;
    container.appendChild(toast);

    // Animate in
    requestAnimationFrame(() => {
        toast.style.opacity = "1";
        toast.style.transform = "translateY(0)";
    });

    // Auto-dismiss after 3.5s
    setTimeout(() => {
        toast.style.opacity = "0";
        toast.style.transform = "translateY(8px)";
        setTimeout(() => toast.remove(), 300);
    }, 3500);
}

/* ── Utility: escape HTML to prevent XSS in CSV preview ─── */
function escapeHtml(str) {
    return String(str)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;");
}
