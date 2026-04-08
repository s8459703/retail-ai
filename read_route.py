content = open('app.py', encoding='utf-8').read()
start = content.find('@app.route("/subcategory')
end = content.find('\n\n\n@app.route', start)
print(content[start:end])
