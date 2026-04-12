import app as a
a.app.config['TESTING'] = True

out = []
out.append("=== ALL ROUTES ===")
for r in sorted(a.app.url_map.iter_rules(), key=lambda x: x.rule):
    if not r.rule.startswith('/static'):
        out.append(f"  {r.rule}")

out.append("\n=== PAGE STATUS ===")
with a.app.test_client() as c:
    with c.session_transaction() as s:
        s['user'] = 'admin'
    pages = [
        ('Dashboard',        '/dashboard'),
        ('Product Analysis', '/product'),
        ('Categories',       '/categories'),
        ('Category Detail',  '/category/Clothing'),
        ('Subcategory',      '/subcategory/Clothing/Men'),
        ('Forecast',         '/future'),
        ('Prediction',       '/predict'),
        ('Filter',           '/filter'),
        ('Upload',           '/upload'),
        ('Settings',         '/settings'),
        ('Profile',          '/profile'),
        ('API Subcategories','/api/subcategories?category=Clothing'),
        ('API Brands',       '/api/brands?category=Clothing&sub_category=Men'),
        ('API Analysis',     '/api/product_analysis?category=Clothing'),
    ]
    for name, route in pages:
        r = c.get(route)
        out.append(f"  {'OK  ' if r.status_code == 200 else 'FAIL'} {r.status_code}  {name:20s}  {route}")

open('project_status.txt', 'w', encoding='utf-8').write('\n'.join(out))
print('\n'.join(out))
