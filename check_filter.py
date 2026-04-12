import glob
for path in glob.glob('templates/*.html'):
    content = open(path, encoding='utf-8').read()
    if 'filter' in content.lower() or 'Filter' in content:
        lines = content.split('\n')
        for i, line in enumerate(lines, 1):
            if 'filter' in line.lower() or 'Filter' in line:
                print(f"{path}:{i}: {line.strip()}")
