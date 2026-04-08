import logging
logging.basicConfig(filename='flask_errors.log', level=logging.DEBUG)

from app import app
app.config['PROPAGATE_EXCEPTIONS'] = False

if __name__ == '__main__':
    app.run(debug=True, port=5000, use_reloader=False)
