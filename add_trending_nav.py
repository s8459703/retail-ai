import glob, subprocess

old = """<a href="{{ url_for('product') }}" class="nav-item"><i class="fas fa-boxes-stacked"></i> Products</a>"""
new = """<a href="{{ url_for('product') }}" class="nav-item"><i class="fas fa-boxes-stacked"></i> Products</a>
            <a href="{{ url_for('trending') }}" class="nav-item"><i class="fas fa-arrow-trend-up"></i> Trending</a>"""

count = 0
for path in glob.glob('templates/*.html'):
    c = open(path, encoding='utf-8').read()
    if old in c and "url_for('trending')" not in c:
        open(path, 'w', encoding='utf-8').write(c.replace(old, new))
        count += 1
        print(f'Updated: {path}')

print(f'Done: {count} files updated')
