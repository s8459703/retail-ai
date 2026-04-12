content = open('static/js/dashboard.js', encoding='utf-8').read()

# Find the function boundaries
start = content.find('function initCharts()')
end   = content.find('\n/* ', start)
if end == -1:
    end = content.find('\n/* \u2550\u2550', start + 100)

old_func = content[start:end]

new_func = r"""function initCharts() {
    const style      = getComputedStyle(document.documentElement);
    const accentFrom = style.getPropertyValue("--accent-from").trim() || "#6366f1";
    const accentRgb  = style.getPropertyValue("--accent-rgb").trim()  || "99,102,241";
    const tickColor  = style.getPropertyValue("--text-faint").trim()  || "#888";
    const textMuted  = style.getPropertyValue("--text-muted").trim()  || "rgba(255,255,255,0.75)";
    const PALETTE    = [accentFrom,"#8b5cf6","#f093fb","#4facfe","#43e97b","#fa709a","#fee140","#30cfd0","#a18cd1","#fda085"];
    const darkGrid   = "rgba(255,255,255,0.05)";
    const lo         = { labels: { color: textMuted, padding: 16 } };
    const tick       = (v) => "\u20b9" + v.toLocaleString();
    const xs         = { ticks: { color: tickColor }, grid: { color: darkGrid } };
    const ys         = { ticks: { color: tickColor, callback: tick }, grid: { color: darkGrid } };

    function read(id) {
        const el = document.getElementById(id);
        if (!el) return [];
        try { return JSON.parse(el.textContent); } catch(e) { return []; }
    }

    function bar(id, labels, data, color, rgb) {
        const el = document.getElementById(id);
        if (!el || !labels || !labels.length) return;
        new Chart(el, {
            type: "bar",
            data: { labels, datasets: [{ label: "Revenue (\u20b9)", data,
                backgroundColor: "rgba(" + rgb + ",0.75)", borderColor: color,
                borderWidth: 1, borderRadius: 6 }] },
            options: { responsive: true, maintainAspectRatio: true,
                plugins: { legend: lo }, scales: { x: xs, y: ys } }
        });
    }

    function donut(id, labels, data, colors) {
        const el = document.getElementById(id);
        if (!el || !labels || !labels.length) return;
        new Chart(el, {
            type: "doughnut",
            data: { labels, datasets: [{ data,
                backgroundColor: colors || PALETTE,
                borderWidth: 2, borderColor: "rgba(15,15,35,0.8)" }] },
            options: { responsive: true, maintainAspectRatio: true,
                plugins: { legend: lo } }
        });
    }

    function line(id, labels, data, color, rgb) {
        const el = document.getElementById(id);
        if (!el || !labels || !labels.length) return;
        new Chart(el, {
            type: "line",
            data: { labels, datasets: [{ label: "Revenue (\u20b9)", data,
                borderColor: color, backgroundColor: "rgba(" + rgb + ",0.12)",
                borderWidth: 2, pointBackgroundColor: color,
                pointRadius: 4, tension: 0.4, fill: true }] },
            options: { responsive: true, maintainAspectRatio: true,
                plugins: { legend: lo }, scales: { x: xs, y: ys } }
        });
    }

    // Dashboard
    bar  ("barChart",    read("data-categories"),    read("data-category-sales"), accentFrom, accentRgb);
    donut("pieChart",    read("data-categories"),    read("data-category-sales"));
    line ("lineChart",   read("data-monthly-labels"),read("data-monthly-sales"),  accentFrom, accentRgb);
    donut("genderChart", read("data-gender-labels"), read("data-gender-values"),  ["#f093fb","#4facfe"]);
    bar  ("cityChart",   read("data-city-labels"),   read("data-city-sales"),     "#4facfe",  "79,172,254");
    bar  ("brandChart",  read("data-brand-labels"),  read("data-brand-sales"),    "#f093fb",  "240,147,251");
}"""

if old_func:
    content = content.replace(old_func, new_func)
    open('static/js/dashboard.js', 'w', encoding='utf-8').write(content)
    print(f"SUCCESS: replaced {len(old_func)} chars with {len(new_func)} chars")
else:
    print("ERROR: could not find initCharts function")
    print("start:", start, "end:", end)
