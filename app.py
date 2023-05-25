from flask import Flask, request, json
from werkzeug.utils import secure_filename
from werkzeug.exceptions import HTTPException
from flask_cors import CORS
import os
import logging
from deepface import DeepFace

app = Flask(__name__)
app.config['UPLOAD_PATH'] = 'temp'
file_handler = logging.FileHandler('server.log')
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


@app.route('/api/compare-faces', methods=['POST'])
def compare_faces():
    if 'unknown' not in request.files or 'original_image' not in request.files:
        return app.response_class(
            response=json.dumps({"error": "Missing files in the request"}),
            status=400,
            mimetype='application/json'
        )

    unknown_file = request.files['unknown']
    original_file = request.files['original_image']

    if not unknown_file.filename or not original_file.filename:
        return app.response_class(
            response=json.dumps({"error": "Empty files in the request"}),
            status=400,
            mimetype='application/json'
        )

    unknown_filename = secure_filename(unknown_file.filename)
    original_filename = secure_filename(original_file.filename)

    unknown_filepath = os.path.join(
        app.config['UPLOAD_PATH'],
        unknown_filename,
    )
    original_filepath = os.path.join(
        app.config['UPLOAD_PATH'],
        original_filename,
    )

    unknown_file.save(unknown_filepath)
    original_file.save(original_filepath)

    try:
        is_same_user = DeepFace.verify(
            original_filepath,
            unknown_filepath,
        )['verified']
    except ValueError:
        print('Value error')
        is_same_user = False

    remove_file(original_filepath)
    remove_file(unknown_filepath)

    return app.response_class(
        response=json.dumps({
            "is_same_user": bool(is_same_user)
        }),
        status=200,
        mimetype='application/json'
    )


def remove_file(filepath):
    if os.path.isfile(filepath):
        os.remove(filepath)
        print("File has been deleted:", filepath)
    else:
        print("File does not exist:", filepath)


@app.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument(
        '-p',
        '--port',
        default=5001,
        type=int,
        help='Port to listen on',
    )
    args = parser.parse_args()
    port = args.port
    host = '127.0.0.1'

    app.run(host=host, port=port, debug=True)
