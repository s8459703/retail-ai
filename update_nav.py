import os, glob

templates = glob.glob('templates/*.html')
count = 0
for path in templates:
    content = open(path, encoding='utf-8').read()
    changed = False

    # Replace filter link with products link
    replacements = [
        (
            '<a href="/filter" class="nav-item"><i class="fas fa-filter"></i> Filter &amp; Explore</a>',
            '<a href="/categories" class="nav-item"><i class="fas fa-boxes-stacked"></i> Products</a>'
        ),
        (
            "<a href=\"/filter\" class=\"nav-item\"><i class=\"fas fa-filter\"></i> Filter &amp; Explore</a>",
            "<a href=\"/categories\" class=\"nav-item\"><i class=\"fas fa-boxes-stacked\"></i> Products</a>"
        ),
        (
            'href="/filter"',
            'href="/categories"'
        ),
        (
            "href=\"/filter\"",
            "href=\"/categories\""
        ),
    ]

    for old, new in replacements:
        if old in content:
            content = content.replace(old, new)
            changed = True

    if changed:
        open(path, 'w', encoding='utf-8').write(content)
        count += 1
        print(f'Updated: {path}')

print(f'\nDone. {count} files updated.')
