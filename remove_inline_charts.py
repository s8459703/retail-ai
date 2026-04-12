content = open('templates/dashboard.html', encoding='utf-8').read()

# Remove the inline <script> block that duplicates chart rendering
start = content.find('\n    <script>\n    document.addEventListener("DOMContentLoaded", () => {')
if start == -1:
    start = content.find('\n    <script>\r\ndocument.addEventListener')
if start == -1:
    start = content.rfind('<script>')
    # Only remove if it's the inline chart script, not dashboard.js loader
    chunk = content[start:start+100]
    if 'DOMContentLoaded' in chunk or 'genderChart' in chunk or 'cityChart' in chunk:
        end = content.rfind('</script>') + len('</script>')
        removed = content[start:end]
        content = content[:start] + content[end:]
        open('templates/dashboard.html', 'w', encoding='utf-8').write(content)
        print(f"Removed inline script ({len(removed)} chars)")
    else:
        print("No inline chart script found to remove")
else:
    end = content.find('</script>', start) + len('</script>')
    removed = content[start:end]
    content = content[:start] + content[end:]
    open('templates/dashboard.html', 'w', encoding='utf-8').write(content)
    print(f"Removed inline script ({len(removed)} chars)")
