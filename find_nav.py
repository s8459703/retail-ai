import glob
for path in glob.glob('templates/*.html'):
    c = open(path, encoding='utf-8').read()
    if 'boxes-stacked' not in c and 'nav-item' in c:
        lines = c.split('\n')
        for i, l in enumerate(lines, 1):
            if 'nav-item' in l:
                print(f"{path}:{i}: {repr(l.strip())}")
        print()
