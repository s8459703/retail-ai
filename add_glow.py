glow_css = """
/* ═══════════════════════════════════════════════════════════
   GLOW / GLASSMORPHISM ENHANCEMENTS
   ═══════════════════════════════════════════════════════════ */

/* ── Page fade-in ────────────────────────────────────────── */
.main-content {
    animation: pageFadeIn 0.5s ease both;
}
@keyframes pageFadeIn {
    from { opacity: 0; transform: translateY(12px); }
    to   { opacity: 1; transform: translateY(0); }
}

/* ── Glowing background orbs ─────────────────────────────── */
body::before,
body::after {
    content: "";
    position: fixed;
    border-radius: 50%;
    filter: blur(120px);
    pointer-events: none;
    z-index: 0;
    opacity: 0.18;
}
body::before {
    width: 600px; height: 600px;
    background: var(--accent-from);
    top: -200px; left: -100px;
}
body::after {
    width: 500px; height: 500px;
    background: var(--accent-to);
    bottom: -150px; right: -100px;
}
[data-theme="light"] body::before,
[data-theme="light"] body::after { opacity: 0.08; }

/* ── Glassmorphism cards ─────────────────────────────────── */
.stat-card,
.chart-card,
.table-card,
.settings-card,
.filter-card {
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    box-shadow: 0 4px 24px rgba(0,0,0,0.18),
                inset 0 1px 0 rgba(255,255,255,0.06);
    transition: transform 0.25s ease, box-shadow 0.25s ease,
                border-color 0.25s ease;
}

/* ── Stat card glow on hover ─────────────────────────────── */
.stat-card:hover {
    transform: translateY(-6px);
    box-shadow: 0 8px 32px rgba(var(--accent-rgb),0.25),
                0 0 0 1px rgba(var(--accent-rgb),0.2),
                inset 0 1px 0 rgba(255,255,255,0.08);
}

/* ── Chart card glow ─────────────────────────────────────── */
.chart-card:hover {
    box-shadow: 0 8px 32px rgba(var(--accent-rgb),0.15),
                0 0 0 1px rgba(var(--accent-rgb),0.15),
                inset 0 1px 0 rgba(255,255,255,0.06);
}

/* ── Glowing stat icon ───────────────────────────────────── */
.stat-icon {
    box-shadow: 0 4px 16px rgba(var(--accent-rgb),0.4);
    transition: box-shadow 0.25s ease, transform 0.25s ease;
}
.stat-card:hover .stat-icon {
    box-shadow: 0 6px 24px rgba(var(--accent-rgb),0.6);
    transform: scale(1.08);
}

/* ── Glowing sidebar nav active ──────────────────────────── */
.nav-item.active {
    background: rgba(var(--accent-rgb),0.15);
    box-shadow: inset 3px 0 0 var(--accent-from),
                0 0 20px rgba(var(--accent-rgb),0.12);
    color: var(--text-primary);
}
.nav-item:hover {
    box-shadow: 0 0 16px rgba(var(--accent-rgb),0.08);
}
.nav-item.active i {
    filter: drop-shadow(0 0 6px var(--accent-from));
}

/* ── Glowing sidebar brand ───────────────────────────────── */
.sidebar-brand {
    text-shadow: 0 0 20px rgba(var(--accent-rgb),0.4);
}

/* ── Glowing primary button ──────────────────────────────── */
.btn.primary {
    box-shadow: 0 4px 20px rgba(var(--accent-rgb),0.4);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.btn.primary:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 32px rgba(var(--accent-rgb),0.6),
                0 0 0 1px rgba(var(--accent-rgb),0.3);
}
.btn.primary:active { transform: translateY(0); }

/* ── Glowing input focus ─────────────────────────────────── */
.settings-input:focus,
.filter-select:focus {
    box-shadow: 0 0 0 3px rgba(var(--accent-rgb),0.2),
                0 0 16px rgba(var(--accent-rgb),0.15);
}

/* ── Glowing table row hover ─────────────────────────────── */
tbody tr:hover td {
    box-shadow: inset 0 0 0 9999px rgba(var(--accent-rgb),0.05);
}

/* ── Glowing category badge ──────────────────────────────── */
.category-badge {
    box-shadow: 0 0 8px rgba(var(--accent-rgb),0.2);
    transition: box-shadow 0.2s ease;
}
.category-badge:hover {
    box-shadow: 0 0 14px rgba(var(--accent-rgb),0.4);
}

/* ── Glowing quick action cards ──────────────────────────── */
.quick-action-card {
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    box-shadow: 0 2px 12px rgba(0,0,0,0.12),
                inset 0 1px 0 rgba(255,255,255,0.04);
}
.quick-action-card:hover {
    box-shadow: 0 8px 28px rgba(var(--accent-rgb),0.2),
                0 0 0 1px rgba(var(--accent-rgb),0.2),
                inset 0 1px 0 rgba(255,255,255,0.06);
}

/* ── Glowing welcome banner ──────────────────────────────── */
.welcome-banner {
    box-shadow: 0 4px 24px rgba(var(--accent-rgb),0.12),
                inset 0 1px 0 rgba(255,255,255,0.06);
    backdrop-filter: blur(12px);
}

/* ── Glowing profile avatar ──────────────────────────────── */
.profile-avatar-lg,
.sidebar-footer .avatar {
    box-shadow: 0 0 20px rgba(var(--accent-rgb),0.5);
}

/* ── Glowing drop zone ───────────────────────────────────── */
.drop-zone:hover,
.drop-zone.drag-over {
    box-shadow: 0 0 24px rgba(var(--accent-rgb),0.2);
}

/* ── Glowing topbar user pill ────────────────────────────── */
.topbar-user {
    box-shadow: 0 2px 12px rgba(0,0,0,0.12);
    transition: box-shadow 0.2s ease;
}
.topbar-user:hover {
    box-shadow: 0 4px 20px rgba(var(--accent-rgb),0.15);
}

/* ── Glowing plan card featured ──────────────────────────── */
.plan-card--featured {
    box-shadow: 0 8px 40px rgba(var(--accent-rgb),0.25),
                0 0 0 1px rgba(var(--accent-rgb),0.3);
}

/* ── Smooth page transitions ─────────────────────────────── */
.nav-item,
.stat-card,
.chart-card,
.table-card,
.btn,
.quick-action-card,
.category-badge {
    transition-property: transform, box-shadow, background, border-color, color;
    transition-duration: 0.25s;
    transition-timing-function: ease;
}

/* ── Light theme glow adjustments ───────────────────────── */
[data-theme="light"] .stat-card:hover {
    box-shadow: 0 8px 32px rgba(var(--accent-rgb),0.15),
                0 0 0 1px rgba(var(--accent-rgb),0.15);
}
[data-theme="light"] .stat-icon {
    box-shadow: 0 4px 16px rgba(var(--accent-rgb),0.25);
}
[data-theme="light"] .stat-card:hover .stat-icon {
    box-shadow: 0 6px 24px rgba(var(--accent-rgb),0.35);
}
[data-theme="light"] .btn.primary {
    box-shadow: 0 4px 16px rgba(var(--accent-rgb),0.3);
}
[data-theme="light"] .btn.primary:hover {
    box-shadow: 0 8px 28px rgba(var(--accent-rgb),0.45);
}
[data-theme="light"] .chart-card,
[data-theme="light"] .table-card,
[data-theme="light"] .settings-card {
    box-shadow: 0 4px 20px rgba(var(--accent-rgb),0.08),
                inset 0 1px 0 rgba(255,255,255,0.8);
}
[data-theme="light"] .sidebar-brand {
    text-shadow: 0 0 16px rgba(var(--accent-rgb),0.2);
}
[data-theme="light"] .nav-item.active i {
    filter: drop-shadow(0 0 4px var(--accent-from));
}
"""

content = open('static/css/dashboard.css', encoding='utf-8').read()
if 'GLOW / GLASSMORPHISM' not in content:
    content += glow_css
    open('static/css/dashboard.css', 'w', encoding='utf-8').write(content)
    print("Glow effects added.")
else:
    # Replace existing glow section
    start = content.find('/* \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\n   GLOW')
    content = content[:start] + glow_css
    open('static/css/dashboard.css', 'w', encoding='utf-8').write(content)
    print("Glow effects replaced.")
