content = open('static/js/dashboard.js', encoding='utf-8').read()
start = content.find('function initCharts')
end = content.find('\n/* ', start)
print(content[start:end])
