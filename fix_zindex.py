content = open('static/css/dashboard.css', encoding='utf-8').read()

fixes = [
    # Ensure canvas stays at z-index 0
    ('#space-canvas {\n    position: fixed; inset: 0;\n    z-index: 0; pointer-events: none;\n}',
     '#space-canvas {\n    position: fixed; inset: 0;\n    z-index: 0; pointer-events: none;\n}'),
]

# Add z-index fix block if not present
zfix = """
/* ── Z-INDEX LAYER FIX ───────────────────────────────────── */
#space-canvas        { position: fixed; inset: 0; z-index: 0 !important; pointer-events: none; }
body::before         { z-index: 0 !important; pointer-events: none; }
body::after          { z-index: 0 !important; pointer-events: none; }
.sidebar             { position: fixed; z-index: 1000 !important; }
.sidebar-overlay     { z-index: 999  !important; }
.sidebar-toggle      { z-index: 1100 !important; }
.main-content        { position: relative; z-index: 1 !important; }
.stat-card,
.chart-card,
.table-card,
.settings-card,
.filter-card,
.quick-action-card,
.welcome-banner,
.profile-hero,
.plan-card           { position: relative; z-index: 1 !important; }
"""

if 'Z-INDEX LAYER FIX' not in content:
    content += zfix
    open('static/css/dashboard.css', 'w', encoding='utf-8').write(content)
    print("Z-index fix added.")
else:
    start = content.find('/* ── Z-INDEX LAYER FIX')
    end   = content.find('\n*/', start) + 3
    content = content[:start] + zfix + content[end:]
    open('static/css/dashboard.css', 'w', encoding='utf-8').write(content)
    print("Z-index fix replaced.")
