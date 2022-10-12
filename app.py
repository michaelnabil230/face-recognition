from flask import Flask, request, json
from werkzeug.utils import secure_filename
from werkzeug.exceptions import HTTPException
from flask_cors import CORS
import face_recognition
import os
import logging

app = Flask(__name__)
app.config['UPLOAD_PATH'] = 'temp'
file_handler = logging.FileHandler('server.log')
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


@app.route('/api/compare-faces', methods=['POST'])
def compare_faces():
    unknown = request.files['unknown']
    original_image = request.files['original_image']

    unknown_filename = os.path.join(
        app.config['UPLOAD_PATH'],
        secure_filename(unknown.filename),
    )

    original_filename = os.path.join(
        app.config['UPLOAD_PATH'],
        secure_filename(original_image.filename),
    )

    unknown.save(unknown_filename)
    original_image.save(original_filename)

    results = face_verification(original_filename, unknown_filename)

    remove_images(original_filename, unknown_filename)

    return app.response_class(
        response=json.dumps({
            "is_same_user": bool(results[0])
        }),
        status=200,
        mimetype='application/json'
    )


def face_verification(original_image_src, unknown_image_src):
    original_image = face_recognition.load_image_file(original_image_src)
    original_image_face_encoding = face_recognition.face_encodings(original_image)[
        0]

    unknown_picture = face_recognition.load_image_file(unknown_image_src)
    unknown_face_encoding = face_recognition.face_encodings(unknown_picture)[0]

    results = face_recognition.compare_faces(
        [original_image_face_encoding],
        unknown_face_encoding,
    )

    return results


def remove_image(path):
    if os.path.isfile(path):
        os.remove(path)
        print("File has been deleted", path)
    else:
        print("File does not exist", path)


def remove_images(original_image_src, unknown_image_src):
    remove_image(original_image_src)
    remove_image(unknown_image_src)


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
        help='port to listen on',
    )
    args = parser.parse_args()
    port = args.port

    app.run(host='127.0.0.1', port=port, debug=True)
