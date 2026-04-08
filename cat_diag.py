import sys, traceback

out = []
try:
    import app as a
    a.app.config['TESTING'] = True
    a.app.config['PROPAGATE_EXCEPTIONS'] = True

    with a.app.test_client() as c:
        with c.session_transaction() as s:
            s['user'] = 'admin'
        try:
            r = c.get('/categories')
            out.append(f"STATUS: {r.status_code}")
            out.append(r.data.decode('utf-8', errors='replace')[:2000])
        except Exception:
            out.append("EXCEPTION in /categories:")
            out.append(traceback.format_exc())
except Exception:
    out.append("STARTUP ERROR:")
    out.append(traceback.format_exc())

with open("cat_diag.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(out))
