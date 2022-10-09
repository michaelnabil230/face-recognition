from flask import Flask, request, json
from werkzeug.utils import secure_filename
from werkzeug.exceptions import HTTPException
import face_recognition
import os

app = Flask(__name__)
app.config['UPLOAD_PATH'] = 'temp'


@app.route('/api/compare-faces', methods=['POST'])
def compare_faces():

    unknown = request.files['unknown']
    original_image = request.files['original_image']

    unknown_filename = os.path.join(
        app.config['UPLOAD_PATH'], secure_filename(unknown.filename))

    original_filename = os.path.join(
        app.config['UPLOAD_PATH'], secure_filename(original_image.filename))

    unknown.save(unknown_filename)
    original_image.save(original_filename)

    results = face_verification(original_filename, unknown_filename)

    if results[0] == True:
        is_same_user = True
    else:
        is_same_user = False

    return app.response_class(
        response=json.dumps({
            "is_same_user": is_same_user
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


if __name__ == "__main__":
    app.run()
