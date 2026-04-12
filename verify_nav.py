import glob
for path in glob.glob('templates/*.html'):
    c = open(path, encoding='utf-8').read()
    has_products = 'boxes-stacked' in c or '/categories' in c
    has_filter_old = 'fa-filter' in c and 'Filter' in c
    print(f"{'OK  ' if has_products else 'MISS'} {'OLD!' if has_filter_old else '    '} {path}")
