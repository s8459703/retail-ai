import re, os

files = [
    'static/css/dashboard.css',
    'static/css/style.css',
    'static/js/dashboard.js',
]

for f in files:
    content = open(f, encoding='utf-8').read()
    # find hex colors and rgba not using var()
    found = re.findall(r'(?<!var\()#[0-9a-fA-F]{3,6}|rgba?\(\s*\d', content)
    print(f"\n=== {f} ({len(found)} hardcoded) ===")
    lines = content.split('\n')
    for i, line in enumerate(lines, 1):
        if re.search(r'(?<!var\()#[0-9a-fA-F]{3,6}|rgba?\(\s*\d', line):
            print(f"  L{i}: {line.strip()}")
