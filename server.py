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
    validate_lecture(request.json)
    return jsonify(lecture_service.create_lecture(request.json))


@app.route('/lectures/<lectureid>', methods=['GET'])
def get_lecture(lectureid):
    if lectureid is None:
        abort(make_response(jsonify(message="you must supply a lecture id"), 400))
    result = lecture_service.get_lecture(lectureid)
    if result:
        return jsonify(result)
    abort(make_response(jsonify(message="lecture not found"), 404))


@app.route('/')
def index():
    return jsonify({"healthy": 200})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)



