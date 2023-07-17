from flask import Flask, jsonify
from coppermind.common import

app = Flask(__name__.split('.')[0])
PORT = 9090
BIND = '0.0.0.0'
DEBUG = True

app.config.from_object(__name__)


@app.route('/')
def index():
    return 'Coppermind'


@app.route('/ebooks')
def ebooks():
    return jsonify([])


@app.route('/ebooks/<book_id>')
def ebook(book_id):
    return jsonify({})


@app.route('/upload')
def upload():
    pass
