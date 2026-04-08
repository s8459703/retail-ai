import sys, traceback
sys.stdout.reconfigure(encoding='utf-8')

import app as a
a.app.config['TESTING'] = True
a.app.config['PROPAGATE_EXCEPTIONS'] = False

with a.app.test_client() as c:
    with c.session_transaction() as s:
        s['user'] = 'admin'
    r = c.get('/categories')
    print("Status:", r.status_code)
    body = r.data.decode('utf-8', errors='replace')
    print(body[:3000])
