content = open('static/js/dashboard.js', encoding='utf-8').read()

start = content.find('function initCharts()')
end   = content.find('\n/* ', start + 50)
if end == -1:
    end = content.find('\n/* \u2550', start + 50)

new_func = """function initCharts() {
    const style      = getComputedStyle(document.documentElement);
    const accentFrom = style.getPropertyValue("--accent-from").trim() || "#6366f1";
    const accentTo   = style.getPropertyValue("--accent-to").trim()   || "#8b5cf6";
    const accentRgb  = style.getPropertyValue("--accent-rgb").trim()  || "99,102,241";
    const tickColor  = style.getPropertyValue("--text-faint").trim()  || "#888";
    const textMuted  = style.getPropertyValue("--text-muted").trim()  || "rgba(255,255,255,0.75)";
    const PALETTE    = [accentFrom, accentTo, "#f093fb", "#4facfe", "#43e97b", "#fa709a", "#fee140", "#30cfd0", "#a18cd1", "#fda085"];
    const darkGrid   = "rgba(255,255,255,0.04)";
    const lo         = { labels: { color: textMuted, padding: 16, font: { size: 12 } } };
    const tick       = (v) => "\\u20b9" + v.toLocaleString();
    const xs         = { ticks: { color: tickColor }, grid: { color: darkGrid } };
    const ys         = { ticks: { color: tickColor, callback: tick }, grid: { color: darkGrid } };

    function read(id) {
        const el = document.getElementById(id);
        if (!el) return [];
        try { return JSON.parse(el.textContent); } catch(e) { return []; }
    }

    function gradient(el, rgb, alpha1, alpha2) {
        try {
            const ctx = el.getContext("2d");
            const h   = el.parentElement ? el.parentElement.offsetHeight : 300;
            const g   = ctx.createLinearGradient(0, 0, 0, h);
            g.addColorStop(0,   "rgba(" + rgb + "," + alpha1 + ")");
            g.addColorStop(1,   "rgba(" + rgb + "," + alpha2 + ")");
            return g;
        } catch(e) { return "rgba(" + rgb + ",0.7)"; }
    }

    function bar(id, labels, data, color, rgb) {
        const el = document.getElementById(id);
        if (!el || !labels || !labels.length) return;
        new Chart(el, {
            type: "bar",
            data: { labels, datasets: [{ label: "Revenue (\\u20b9)", data,
                backgroundColor: gradient(el, rgb, 0.85, 0.25),
                borderColor: color, borderWidth: 1, borderRadius: 10,
                hoverBackgroundColor: "rgba(" + rgb + ",1)",
                hoverBorderColor: color, hoverBorderWidth: 2 }] },
            options: { responsive: true, maintainAspectRatio: true,
                animation: { duration: 900, easing: "easeOutQuart" },
                plugins: { legend: lo },
                scales: { x: xs, y: ys } }
        });
    }

    function donut(id, labels, data, colors) {
        const el = document.getElementById(id);
        if (!el || !labels || !labels.length) return;
        new Chart(el, {
            type: "doughnut",
            data: { labels, datasets: [{ data,
                backgroundColor: colors || PALETTE,
                borderWidth: 3,
                borderColor: "rgba(10,10,30,0.6)",
                hoverOffset: 8 }] },
            options: { responsive: true, maintainAspectRatio: true,
                animation: { duration: 900, easing: "easeOutQuart" },
                plugins: { legend: lo } }
        });
    }

    function line(id, labels, data, color, rgb) {
        const el = document.getElementById(id);
        if (!el || !labels || !labels.length) return;
        const ctx = el.getContext("2d");
        const fillGrad = ctx.createLinearGradient(0, 0, 0, el.parentElement ? el.parentElement.offsetHeight : 300);
        fillGrad.addColorStop(0, "rgba(" + rgb + ",0.35)");
        fillGrad.addColorStop(1, "rgba(" + rgb + ",0.0)");
        new Chart(el, {
            type: "line",
            data: { labels, datasets: [{ label: "Revenue (\\u20b9)", data,
                borderColor: color,
                backgroundColor: fillGrad,
                borderWidth: 2.5,
                pointBackgroundColor: color,
                pointBorderColor: "rgba(10,10,30,0.8)",
                pointBorderWidth: 2,
                pointRadius: 5,
                pointHoverRadius: 8,
                tension: 0.45, fill: true }] },
            options: { responsive: true, maintainAspectRatio: true,
                animation: { duration: 900, easing: "easeOutQuart" },
                plugins: { legend: lo },
                scales: { x: xs, y: ys } }
        });
    }

    // Dashboard charts
    bar  ("barChart",    read("data-categories"),    read("data-category-sales"), accentFrom, accentRgb);
    donut("pieChart",    read("data-categories"),    read("data-category-sales"));
    line ("lineChart",   read("data-monthly-labels"),read("data-monthly-sales"),  accentFrom, accentRgb);
    donut("genderChart", read("data-gender-labels"), read("data-gender-values"),  ["#f093fb","#4facfe"]);
    bar  ("cityChart",   read("data-city-labels"),   read("data-city-sales"),     "#4facfe",  "79,172,254");
    bar  ("brandChart",  read("data-brand-labels"),  read("data-brand-sales"),    "#f093fb",  "240,147,251");
}"""

old_func = content[start:end]
content  = content.replace(old_func, new_func)
open('static/js/dashboard.js', 'w', encoding='utf-8').write(content)
print(f"initCharts rewritten ({len(old_func)} -> {len(new_func)} chars)")
