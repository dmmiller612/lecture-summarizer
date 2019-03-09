from flask import Flask
from flask import request, jsonify, abort, make_response
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/lectures', methods=['POST'])
def create():
    pass

@app.route('/')
def index():
    return jsonify({"healthy": 200})

