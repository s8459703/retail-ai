space_css = """
/* ═══════════════════════════════════════════════════════════
   SPACE / FUTURISTIC THEME
   ═══════════════════════════════════════════════════════════ */

/* ── Futuristic font ─────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;700;900&family=Inter:wght@300;400;500;600;700;800&display=swap');

:root {
    --font-display: 'Orbitron', sans-serif;
    --font-body:    'Inter', sans-serif;
}

body {
    font-family: var(--font-body);
    background: #050510;
    overflow-x: hidden;
}

/* ── Star particle canvas ────────────────────────────────── */
#space-canvas {
    position: fixed;
    inset: 0;
    z-index: 0;
    pointer-events: none;
}

.sidebar,
.main-content {
    position: relative;
    z-index: 1;
}

/* ── Deep space background ───────────────────────────────── */
body::before {
    content: "";
    position: fixed;
    inset: 0;
    background:
        radial-gradient(ellipse 80% 60% at 20% 10%, rgba(99,102,241,0.18) 0%, transparent 60%),
        radial-gradient(ellipse 60% 50% at 80% 80%, rgba(139,92,246,0.15) 0%, transparent 60%),
        radial-gradient(ellipse 40% 40% at 50% 50%, rgba(14,165,233,0.08) 0%, transparent 70%),
        linear-gradient(135deg, #050510 0%, #0a0f2c 50%, #120d2b 100%);
    z-index: 0;
    pointer-events: none;
}
body::after { display: none; }

/* ── Futuristic headings ─────────────────────────────────── */
.sidebar-brand,
.page-header h1,
.topbar-left h2 {
    font-family: var(--font-display);
    letter-spacing: 0.05em;
}

.sidebar-brand {
    font-size: 1.1rem;
    background: linear-gradient(90deg, #6366f1, #a78bfa, #38bdf8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    text-shadow: none;
    filter: drop-shadow(0 0 12px rgba(99,102,241,0.6));
}

.page-header h1 {
    font-size: 1.8rem;
    background: linear-gradient(90deg, #e0e7ff, #a78bfa, #38bdf8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    filter: drop-shadow(0 0 16px rgba(99,102,241,0.4));
}

.topbar-left h2 {
    font-size: 1.3rem;
    background: linear-gradient(90deg, #c7d2fe, #a78bfa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

/* ── Neon sidebar ────────────────────────────────────────── */
.sidebar {
    background: rgba(5,5,20,0.85);
    border-right: 1px solid rgba(99,102,241,0.2);
    box-shadow: 4px 0 40px rgba(99,102,241,0.08);
}

.nav-item {
    font-family: var(--font-body);
    font-size: 0.875rem;
    letter-spacing: 0.02em;
    border-radius: 10px;
    transition: all 0.25s ease;
}

.nav-item:hover {
    background: rgba(99,102,241,0.12);
    color: #c7d2fe;
    padding-left: 1.5rem;
    box-shadow: inset 0 0 20px rgba(99,102,241,0.08),
                0 0 12px rgba(99,102,241,0.1);
}

.nav-item.active {
    background: rgba(99,102,241,0.18);
    color: #e0e7ff;
    border-left: 2px solid #6366f1;
    box-shadow: inset 0 0 30px rgba(99,102,241,0.12),
                0 0 20px rgba(99,102,241,0.15),
                4px 0 20px rgba(99,102,241,0.1);
}

.nav-item.active i {
    color: #818cf8;
    filter: drop-shadow(0 0 8px #6366f1);
}

.nav-item i {
    transition: filter 0.25s ease, color 0.25s ease;
}

.nav-item:hover i {
    color: #a5b4fc;
    filter: drop-shadow(0 0 6px rgba(99,102,241,0.8));
}

/* ── Glassmorphism cards ─────────────────────────────────── */
.stat-card,
.chart-card,
.table-card,
.settings-card,
.filter-card {
    background: rgba(10,15,44,0.6);
    border: 1px solid rgba(99,102,241,0.2);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    box-shadow:
        0 4px 24px rgba(0,0,0,0.4),
        0 0 0 1px rgba(99,102,241,0.08),
        inset 0 1px 0 rgba(255,255,255,0.05);
    transition: transform 0.3s ease, box-shadow 0.3s ease, border-color 0.3s ease;
}

.stat-card:hover {
    transform: translateY(-8px) scale(1.01);
    border-color: rgba(99,102,241,0.5);
    box-shadow:
        0 16px 48px rgba(0,0,0,0.5),
        0 0 30px rgba(99,102,241,0.25),
        0 0 60px rgba(99,102,241,0.1),
        inset 0 1px 0 rgba(255,255,255,0.08);
}

.chart-card:hover,
.table-card:hover {
    border-color: rgba(99,102,241,0.35);
    box-shadow:
        0 8px 32px rgba(0,0,0,0.4),
        0 0 20px rgba(99,102,241,0.15),
        inset 0 1px 0 rgba(255,255,255,0.06);
}

/* ── Neon stat icon ──────────────────────────────────────── */
.stat-icon {
    background: linear-gradient(135deg, rgba(99,102,241,0.3), rgba(139,92,246,0.3));
    border: 1px solid rgba(99,102,241,0.4);
    box-shadow:
        0 0 20px rgba(99,102,241,0.4),
        inset 0 0 20px rgba(99,102,241,0.1);
    transition: box-shadow 0.3s ease, transform 0.3s ease;
}

.stat-card:hover .stat-icon {
    box-shadow:
        0 0 30px rgba(99,102,241,0.7),
        0 0 60px rgba(99,102,241,0.3),
        inset 0 0 20px rgba(99,102,241,0.2);
    transform: scale(1.1) rotate(5deg);
}

/* ── Neon stat values ────────────────────────────────────── */
.stat-value {
    font-family: var(--font-display);
    font-size: 1.5rem !important;
    background: linear-gradient(90deg, #e0e7ff, #a78bfa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.stat-label {
    font-size: 0.75rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: rgba(148,163,184,0.7) !important;
}

/* ── Neon chart headings ─────────────────────────────────── */
.chart-card h3,
.table-card h3 {
    font-family: var(--font-display);
    font-size: 0.85rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #a5b4fc;
}

.chart-card h3 i,
.table-card h3 i {
    filter: drop-shadow(0 0 6px currentColor);
}

/* ── Neon table ──────────────────────────────────────────── */
thead th {
    font-family: var(--font-display);
    font-size: 0.65rem;
    letter-spacing: 0.12em;
    color: rgba(99,102,241,0.8) !important;
    border-bottom: 1px solid rgba(99,102,241,0.2) !important;
}

tbody td {
    color: rgba(203,213,225,0.85);
    border-bottom: 1px solid rgba(99,102,241,0.06) !important;
}

tbody tr:hover td {
    background: rgba(99,102,241,0.06) !important;
    color: #e0e7ff;
}

/* ── Neon buttons ────────────────────────────────────────── */
.btn.primary {
    background: linear-gradient(135deg, #4f46e5, #7c3aed);
    border: 1px solid rgba(99,102,241,0.5);
    box-shadow:
        0 4px 20px rgba(99,102,241,0.4),
        0 0 0 1px rgba(99,102,241,0.2),
        inset 0 1px 0 rgba(255,255,255,0.1);
    font-family: var(--font-body);
    letter-spacing: 0.03em;
    position: relative;
    overflow: hidden;
}

.btn.primary::after {
    content: "";
    position: absolute;
    inset: 0;
    background: linear-gradient(135deg, rgba(255,255,255,0.1), transparent);
    opacity: 0;
    transition: opacity 0.3s ease;
}

.btn.primary:hover::after { opacity: 1; }

.btn.primary:hover {
    transform: translateY(-3px);
    box-shadow:
        0 8px 32px rgba(99,102,241,0.6),
        0 0 60px rgba(99,102,241,0.2),
        0 0 0 1px rgba(99,102,241,0.4),
        inset 0 1px 0 rgba(255,255,255,0.15);
}

/* ── Neon topbar ─────────────────────────────────────────── */
.topbar-user,
.topbar-date {
    background: rgba(10,15,44,0.7);
    border: 1px solid rgba(99,102,241,0.2);
    backdrop-filter: blur(10px);
    color: #a5b4fc;
}

/* ── Neon category badge ─────────────────────────────────── */
.category-badge {
    background: rgba(99,102,241,0.15);
    border: 1px solid rgba(99,102,241,0.35);
    color: #a5b4fc;
    box-shadow: 0 0 10px rgba(99,102,241,0.2);
    font-family: var(--font-body);
    font-size: 0.75rem;
    letter-spacing: 0.04em;
}

/* ── Neon text highlight ─────────────────────────────────── */
.text-highlight {
    color: #818cf8;
    text-shadow: 0 0 10px rgba(99,102,241,0.5);
}

/* ── Neon section heading ────────────────────────────────── */
.section-heading {
    font-family: var(--font-display);
    font-size: 0.65rem;
    letter-spacing: 0.15em;
    color: rgba(99,102,241,0.8);
}

/* ── Neon welcome banner ─────────────────────────────────── */
.welcome-banner {
    background: rgba(10,15,44,0.6);
    border: 1px solid rgba(99,102,241,0.25);
    backdrop-filter: blur(20px);
    box-shadow:
        0 4px 24px rgba(0,0,0,0.3),
        0 0 40px rgba(99,102,241,0.08);
}

.welcome-banner-text h1 {
    font-family: var(--font-display);
    font-size: 1.3rem;
    background: linear-gradient(90deg, #e0e7ff, #a78bfa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

/* ── Neon quick action cards ─────────────────────────────── */
.quick-action-card {
    background: rgba(10,15,44,0.5);
    border: 1px solid rgba(99,102,241,0.15);
    backdrop-filter: blur(12px);
    transition: all 0.3s ease;
}

.quick-action-card:hover {
    border-color: rgba(99,102,241,0.45);
    transform: translateY(-4px);
    box-shadow:
        0 12px 32px rgba(0,0,0,0.4),
        0 0 24px rgba(99,102,241,0.2);
}

.qa-title { color: #e0e7ff; }
.qa-desc  { color: rgba(148,163,184,0.7); font-size: 0.78rem; }

/* ── Neon sidebar footer ─────────────────────────────────── */
.sidebar-footer {
    border-top: 1px solid rgba(99,102,241,0.15);
}

.sidebar-footer .user-name { color: #c7d2fe; }
.sidebar-footer .user-role { color: rgba(99,102,241,0.6); font-size: 0.7rem; letter-spacing: 0.06em; }

/* ── Neon scrollbar ──────────────────────────────────────── */
::-webkit-scrollbar-track { background: rgba(5,5,20,0.5); }
::-webkit-scrollbar-thumb { background: rgba(99,102,241,0.3); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: rgba(99,102,241,0.6); }

/* ── Pulse animation on stat cards ──────────────────────── */
@keyframes neonPulse {
    0%, 100% { box-shadow: 0 4px 24px rgba(0,0,0,0.4), 0 0 0 1px rgba(99,102,241,0.08), inset 0 1px 0 rgba(255,255,255,0.05); }
    50%       { box-shadow: 0 4px 24px rgba(0,0,0,0.4), 0 0 20px rgba(99,102,241,0.15), 0 0 0 1px rgba(99,102,241,0.15), inset 0 1px 0 rgba(255,255,255,0.05); }
}

.stat-card { animation: neonPulse 4s ease-in-out infinite; }
.stat-card:nth-child(2) { animation-delay: 0.5s; }
.stat-card:nth-child(3) { animation-delay: 1s; }
.stat-card:nth-child(4) { animation-delay: 1.5s; }

/* ── Animated gradient border on chart cards ─────────────── */
@keyframes borderGlow {
    0%, 100% { border-color: rgba(99,102,241,0.2); }
    50%       { border-color: rgba(139,92,246,0.4); }
}

.chart-card { animation: borderGlow 6s ease-in-out infinite; }

/* ── Page load animation ─────────────────────────────────── */
.main-content {
    animation: spaceFadeIn 0.7s ease both;
}

@keyframes spaceFadeIn {
    from { opacity: 0; transform: translateY(20px) scale(0.99); }
    to   { opacity: 1; transform: translateY(0)    scale(1); }
}

/* ── Neon filter/settings inputs ─────────────────────────── */
.settings-input,
.filter-select {
    background: rgba(10,15,44,0.7);
    border: 1px solid rgba(99,102,241,0.25);
    color: #e0e7ff;
    font-family: var(--font-body);
}

.settings-input:focus,
.filter-select:focus {
    border-color: rgba(99,102,241,0.6);
    box-shadow: 0 0 0 3px rgba(99,102,241,0.15), 0 0 20px rgba(99,102,241,0.2);
    outline: none;
}

.filter-select option { background: #0a0f2c; color: #e0e7ff; }

/* ── Neon toggle switch ──────────────────────────────────── */
.toggle-switch input:checked + .toggle-track {
    background: linear-gradient(135deg, #4f46e5, #7c3aed);
    box-shadow: 0 0 12px rgba(99,102,241,0.5);
}

/* ── Neon plan card featured ─────────────────────────────── */
.plan-card--featured {
    border-color: rgba(99,102,241,0.5);
    box-shadow:
        0 8px 40px rgba(0,0,0,0.5),
        0 0 40px rgba(99,102,241,0.2),
        0 0 80px rgba(99,102,241,0.08);
}

/* ── Neon drop zone ──────────────────────────────────────── */
.drop-zone {
    background: rgba(10,15,44,0.4);
    border-color: rgba(99,102,241,0.3);
}

.drop-zone:hover {
    background: rgba(99,102,241,0.06);
    border-color: rgba(99,102,241,0.6);
    box-shadow: 0 0 30px rgba(99,102,241,0.15);
}

/* ── Neon profile hero ───────────────────────────────────── */
.profile-hero {
    background: rgba(10,15,44,0.6);
    border: 1px solid rgba(99,102,241,0.2);
    backdrop-filter: blur(20px);
}

.profile-name {
    font-family: var(--font-display);
    background: linear-gradient(90deg, #e0e7ff, #a78bfa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
"""

content = open('static/css/dashboard.css', encoding='utf-8').read()
marker = '/* \u2550\u2550\u2550 SPACE / FUTURISTIC'
if marker not in content:
    content += '\n' + space_css
    open('static/css/dashboard.css', 'w', encoding='utf-8').write(content)
    print("Space theme CSS added.")
else:
    start = content.find(marker)
    content = content[:start] + '\n' + space_css
    open('static/css/dashboard.css', 'w', encoding='utf-8').write(content)
    print("Space theme CSS replaced.")
