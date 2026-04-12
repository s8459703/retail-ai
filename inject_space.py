import glob

FONT_TAG   = '    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;700;900&family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">'
SCRIPT_TAG = '    <script src="{{ url_for(\'static\', filename=\'js/space-particles.js\') }}" defer></script>'

inner_templates = [
    'templates/dashboard.html',
    'templates/home.html',
    'templates/predict.html',
    'templates/future.html',
    'templates/profile.html',
    'templates/settings.html',
    'templates/upload.html',
    'templates/premium.html',
    'templates/categories.html',
    'templates/category.html',
    'templates/analysis.html',
    'templates/filter.html',
    'templates/product.html',
]

for path in inner_templates:
    try:
        content = open(path, encoding='utf-8').read()
        changed = False

        # Add Orbitron font after charset meta
        if 'Orbitron' not in content:
            content = content.replace(
                '    <link rel="stylesheet" href="{{ url_for(\'static\', filename=\'css/dashboard.css\') }}">',
                FONT_TAG + '\n    <link rel="stylesheet" href="{{ url_for(\'static\', filename=\'css/dashboard.css\') }}">'
            )
            changed = True

        # Add space particles before </body>
        if 'space-particles' not in content:
            content = content.replace(
                '\n</body>',
                '\n' + SCRIPT_TAG + '\n</body>'
            )
            changed = True

        if changed:
            open(path, 'w', encoding='utf-8').write(content)
            print(f'Updated: {path}')
        else:
            print(f'Already OK: {path}')
    except Exception as e:
        print(f'Error {path}: {e}')
