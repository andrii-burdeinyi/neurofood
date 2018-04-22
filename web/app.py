import os

from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello Neurofood!'


@app.route('/train', methods=['POST'])
def train():
    return 'Neurofood has been trained'


@app.route('/run', methods=['POST'])
def run():
    return 'Neiurofood has been run'


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 80.
    port = int(os.environ.get('PORT', os.getenv('CONTAINER_FLASK_PORT', 80)))
    app.run(host='0.0.0.0', port=port, debug=os.getenv('FLASK_DEBUG', False))
