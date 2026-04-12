import app as a
a.app.config['TESTING'] = True
with a.app.test_client() as c:
    with c.session_transaction() as s:
        s['user'] = 'admin'
    r = c.get('/dashboard')
    body = r.data.decode('utf-8', 'replace')

    # Check data islands
    import re
    islands = re.findall(r'<script id="(data-[^"]+)"[^>]*>([^<]{0,80})', body)
    print("=== DATA ISLANDS ===")
    for id_, val in islands:
        print(f"  {id_}: {val[:60]}")

    # Check canvas IDs
    canvases = re.findall(r'<canvas id="([^"]+)"', body)
    print("\n=== CANVAS IDs ===")
    for c in canvases:
        print(f"  {c}")

    # Check Chart.js script tag
    print("\n=== CHART.JS LOADED ===")
    print("  Yes" if 'chart.js' in body.lower() else "  NO - MISSING!")

    # Check dashboard.js
    print("\n=== DASHBOARD.JS LOADED ===")
    print("  Yes" if 'dashboard.js' in body else "  NO - MISSING!")

open('chart_debug.txt', 'w', encoding='utf-8').write(body[:5000])
print("\nFirst 5000 chars saved to chart_debug.txt")
