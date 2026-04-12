import app as a
a.app.config['TESTING'] = True
out = []
with a.app.test_client() as c:
    with c.session_transaction() as s:
        s['user'] = 'admin'
    for route in [
        '/product',
        '/api/subcategories?category=Clothing',
        '/api/brands?category=Clothing&sub_category=Men',
        '/api/product_analysis?category=Clothing&sub_category=Men',
    ]:
        r = c.get(route)
        out.append(f"{r.status_code}  {route}  {r.data.decode('utf-8','replace')[:80]}")
open('prod_check.txt','w',encoding='utf-8').write('\n'.join(out))
