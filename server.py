from flask import Flask
from flask import request, jsonify, abort, make_response
from flask_cors import CORS
from summarizer.LectureService import LectureService

app = Flask(__name__)
CORS(app)

lecture_service = LectureService()


def validate_lecture(request):
    if 'course' not in request or not request['course']:
        abort(make_response(jsonify(message="course must be supplied"), 400))
    if 'content' not in request or not request['content']:
        abort(make_response(jsonify(message="content must be supplied"), 400))
    if 'name' not in request or not request['name']:
        abort(make_response(jsonify(message="name must be supplied"), 400))


@app.route('/lectures', methods=['POST'])
def create():
    validate_lecture(request)
    return jsonify(lecture_service.create_lecture(request))


@app.route('/')
def index():
    return jsonify({"healthy": 200})



