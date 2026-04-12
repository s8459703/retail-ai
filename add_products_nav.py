import glob

# Templates that have a sidebar with Upload Data link
sidebar_templates = [
    'templates/category.html',
    'templates/future.html',
    'templates/home.html',
    'templates/predict.html',
    'templates/premium.html',
    'templates/profile.html',
    'templates/settings.html',
    'templates/upload.html',
    'templates/filter.html',
]

# The Upload Data nav item is the anchor point - insert Products before it
OLD = '<a href="/upload" class="nav-item"><i class="fas fa-upload"></i> Upload Data</a>'
NEW = '<a href="/categories" class="nav-item"><i class="fas fa-boxes-stacked"></i> Products</a>\n            <a href="/upload" class="nav-item"><i class="fas fa-upload"></i> Upload Data</a>'

count = 0
for path in sidebar_templates:
    try:
        content = open(path, encoding='utf-8').read()
        if OLD in content and 'boxes-stacked' not in content:
            content = content.replace(OLD, NEW)
            open(path, 'w', encoding='utf-8').write(content)
            count += 1
            print(f'Updated: {path}')
        elif 'boxes-stacked' in content:
            print(f'Already OK: {path}')
        else:
            print(f'No anchor found: {path}')
    except Exception as e:
        print(f'Error {path}: {e}')

print(f'\nDone. {count} files updated.')
