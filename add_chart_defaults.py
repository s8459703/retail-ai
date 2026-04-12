content = open('static/js/dashboard.js', encoding='utf-8').read()

patch = """
/* ── Chart.js global glow defaults ──────────────────────── */
document.addEventListener("DOMContentLoaded", function() {
    if (typeof Chart === 'undefined') return;
    Chart.defaults.animation = { duration: 900, easing: 'easeOutQuart' };
    Chart.defaults.plugins.tooltip.backgroundColor = 'rgba(10,10,30,0.92)';
    Chart.defaults.plugins.tooltip.borderColor     = 'rgba(99,102,241,0.35)';
    Chart.defaults.plugins.tooltip.borderWidth     = 1;
    Chart.defaults.plugins.tooltip.padding         = 12;
    Chart.defaults.plugins.tooltip.cornerRadius    = 10;
    Chart.defaults.plugins.tooltip.titleColor      = '#ffffff';
    Chart.defaults.plugins.tooltip.bodyColor       = '#a0a0c0';
    Chart.defaults.plugins.tooltip.displayColors   = true;
    Chart.defaults.plugins.tooltip.boxPadding      = 4;
});
"""

if 'Chart.js global glow defaults' not in content:
    content += patch
    open('static/js/dashboard.js', 'w', encoding='utf-8').write(content)
    print("Chart.js defaults added.")
else:
    print("Already present.")
