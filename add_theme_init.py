import glob

THEME_SCRIPT = '''    <script>
        (function(){
            var t = localStorage.getItem("retailai-theme") || "dark";
            document.documentElement.setAttribute("data-theme", t);
        })();
    </script>'''

public_templates = [
    'templates/index.html',
    'templates/login.html',
    'templates/register.html',
    'templates/welcome.html',
    'templates/error.html',
]

for path in public_templates:
    try:
        content = open(path, encoding='utf-8').read()
        if 'retailai-theme' not in content:
            content = content.replace('</head>', THEME_SCRIPT + '\n</head>', 1)
            open(path, 'w', encoding='utf-8').write(content)
            print(f'Updated: {path}')
        else:
            print(f'Already has theme: {path}')
    except Exception as e:
        print(f'Error {path}: {e}')
