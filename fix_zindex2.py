content = open('static/css/dashboard.css', encoding='utf-8').read()

zfix = """
/* ── Z-INDEX LAYER FIX ───────────────────────────────────── */
#space-canvas        { position: fixed; inset: 0; z-index: -1 !important; pointer-events: none; }
body::before         { z-index: -1 !important; pointer-events: none; }
body::after          { z-index: -1 !important; pointer-events: none; }
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

start = content.find('/* ── Z-INDEX LAYER FIX')
end   = content.find('\n}', start + 50)
# find the last } of the block
block_end = content.find('\n\n', start)
if block_end == -1:
    block_end = len(content)

content = content[:start] + zfix + content[block_end:]
open('static/css/dashboard.css', 'w', encoding='utf-8').write(content)
print("Z-index fix updated with z-index: -1 for canvas.")
