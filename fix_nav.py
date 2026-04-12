import glob

templates = glob.glob('templates/*.html')
old_patterns = [
    ('<a href="/filter" class="nav-item"><i class="fas fa-filter"></i> Filter &amp; Explore</a>',
     '<a href="/categories" class="nav-item"><i class="fas fa-boxes-stacked"></i> Products</a>'),
    ('<a href="{{ url_for(\'filter_view\') }}" class="nav-item"><i class="fas fa-filter"></i> Filter &amp; Explore</a>',
     '<a href="/categories" class="nav-item"><i class="fas fa-boxes-stacked"></i> Products</a>'),
]

for path in templates:
    content = open(path, encoding='utf-8').read()
    changed = False
    for old, new in old_patterns:
        if old in content:
            content = content.replace(old, new)
            changed = True
    if changed:
        open(path, 'w', encoding='utf-8').write(content)
        print(f'Updated: {path}')

print('Done.')
