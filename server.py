from flask import Flask
from flask import request, jsonify, abort, make_response
from flask_cors import CORS
from summarizer.LectureService import LectureService
from summarizer.UdacityParser import UdacityParser
from summarizer.SummarizationService import SummarizationService

app = Flask(__name__)
CORS(app)

lecture_service = LectureService()
summary_service = SummarizationService()


def validate_lecture(request):
    if 'course' not in request or not request['course']:
        abort(make_response(jsonify(message="course must be supplied"), 400))
    if 'content' not in request or not request['content']:
        abort(make_response(jsonify(message="content must be supplied"), 400))
    if 'name' not in request or not request['name']:
        abort(make_response(jsonify(message="name must be supplied"), 400))


@app.route('/udacity', methods=['POST'])
def convert_udacity():
    data = request.data
    if not data:
        abort(make_response(jsonify(message="Request must have raw text"), 400))
    return jsonify(UdacityParser(data).convert_to_paragraphs())


@app.route('/lectures', methods=['POST'])
def create_lecture():
    validate_lecture(request.json)
    return jsonify(lecture_service.create_lecture(request.json))


@app.route('/lectures', methods=['GET'])
def get_lectures():
    course = request.args.get('course', None)
    name = request.args.get('name', None)
    limit = int(request.args.get('limit', 10))
    return jsonify(lecture_service.get_lectures(course, name, limit))


@app.route('/lectures/<lectureid>', methods=['GET'])
def get_lecture(lectureid):
    if lectureid is None:
        abort(make_response(jsonify(message="you must supply a lecture id"), 400))
    result = lecture_service.get_lecture(lectureid)
    if result:
        return jsonify(result)
    abort(make_response(jsonify(message="lecture not found"), 404))


@app.route('/lectures/<lectureid>', methods=['DELETE'])
def delete_lecture(lectureid):
    if lectureid is None:
        abort(make_response(jsonify(message="you must supply a lecture id"), 400))
    result = lecture_service.delete_lecture(lectureid)
    if result:
        return jsonify(result)
    abort(make_response(jsonify(message="lecture not found"), 404))


@app.route('/lectures/<lectureid>/summaries', methods=['POST'])
def create_summary(lectureid):
    if lectureid is None:
        abort(make_response(jsonify(message="you must supply a lecture id"), 400))
    try:
        result = summary_service.create_summary(lectureid, request.json)
        if result:
            return jsonify(result)
    except Exception as e:
        abort(make_response(jsonify(message=str(e)), 400))
    abort(make_response(jsonify(message="lecture not found"), 404))


@app.route('/lectures/<lectureid>/summaries', methods=['GET'])
def get_summaries(lectureid):
    lecture: int = lectureid
    name: str = request.args.get('name', None)
    limit: int = int(request.args.get('limit', 10))
    return jsonify(summary_service.list_summaries(name, lecture, limit))


@app.route('/lectures/<lectureid>/summaries/<summaryid>', methods=['GET'])
def get_summary(lectureid, summaryid):
    if lectureid is None or summaryid is None:
        abort(make_response(jsonify(message="lecture id and summary id must be supplied in URL"), 400))
    summary = summary_service.get_summary(lectureid, summaryid)
    if summary:
        return jsonify(summary)
    abort(make_response(jsonify(message="Summary or lecture not found"), 404))


@app.route('/lectures/<lectureid>/summaries/<summaryid>', methods=['DELETE'])
def delete_summary(lectureid, summaryid):
    if lectureid is None or summaryid is None:
        abort(make_response(jsonify(message="you must supply a lecture id and summary id"), 400))
    result = summary_service.delete_summary(summaryid)
    if result:
        return jsonify(result)
    abort(make_response(jsonify(message="summary or lecture not found"), 404))


@app.route('/')
def index():
    return jsonify({"healthy": 200})


@app.errorhandler(404)
def page_not_found(e):
    return jsonify(error=404, text=str(e)), 404


@app.errorhandler(500)
def page_not_found(e):
    return jsonify(error=500, text='Unexpected Error Occurred'), 500



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)



