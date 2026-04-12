content = open('static/js/dashboard.js', encoding='utf-8').read()

old = '    function bar(id, labels, data, color, rgb) {\r\n        const el = document.getElementById(id);\r\n        if (!el || !labels || !labels.length) return;\r\n        new Chart(el, {\r\n            type: "bar",\r\n            data: { labels, datasets: [{ label: "Revenue (\\u20b9)", data,\r\n                backgroundColor: "rgba(" + rgb + ",0.75)", borderColor: color,\r\n                borderWidth: 1, borderRadius: 6 }] },\r\n            options: { responsive: true, maintainAspectRatio: true,\r\n                plugins: { legend: lo }, scales: { x: xs, y: ys } }\r\n        });\r\n    }'

new = '''    function makeGradient(el, rgb) {
        try {
            const ctx = el.getContext("2d");
            const g = ctx.createLinearGradient(0, 0, 0, el.offsetHeight || 300);
            g.addColorStop(0,   "rgba(" + rgb + ",0.85)");
            g.addColorStop(1,   "rgba(" + rgb + ",0.2)");
            return g;
        } catch(e) { return "rgba(" + rgb + ",0.75)"; }
    }

    function bar(id, labels, data, color, rgb) {
        const el = document.getElementById(id);
        if (!el || !labels || !labels.length) return;
        new Chart(el, {
            type: "bar",
            data: { labels, datasets: [{ label: "Revenue (\\u20b9)", data,
                backgroundColor: makeGradient(el, rgb),
                borderColor: color, borderWidth: 1, borderRadius: 8,
                hoverBackgroundColor: "rgba(" + rgb + ",1)" }] },
            options: { responsive: true, maintainAspectRatio: true,
                animation: { duration: 800, easing: "easeOutQuart" },
                plugins: { legend: lo }, scales: { x: xs, y: ys } }
        });
    }'''

if old in content:
    content = content.replace(old, new)
    open('static/js/dashboard.js', 'w', encoding='utf-8').write(content)
    print("Bar gradient added.")
else:
    # Try LF version
    old_lf = old.replace('\r\n', '\n')
    if old_lf in content:
        content = content.replace(old_lf, new)
        open('static/js/dashboard.js', 'w', encoding='utf-8').write(content)
        print("Bar gradient added (LF).")
    else:
        print("Could not find bar function - adding gradient helper separately")
        # Just add animation to existing charts by appending a patch
        patch = """
/* Chart gradient patch */
document.addEventListener("DOMContentLoaded", function() {
    // Patch Chart.js defaults for animations
    if (typeof Chart !== 'undefined') {
        Chart.defaults.animation = { duration: 800, easing: 'easeOutQuart' };
        Chart.defaults.plugins.tooltip.backgroundColor = 'rgba(15,15,35,0.9)';
        Chart.defaults.plugins.tooltip.borderColor = 'rgba(99,102,241,0.3)';
        Chart.defaults.plugins.tooltip.borderWidth = 1;
        Chart.defaults.plugins.tooltip.padding = 10;
        Chart.defaults.plugins.tooltip.cornerRadius = 8;
    }
});
"""
        content += patch
        open('static/js/dashboard.js', 'w', encoding='utf-8').write(content)
        print("Chart defaults patch added.")
