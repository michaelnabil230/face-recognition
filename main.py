import face_recognition
import argparse

parser = argparse.ArgumentParser(
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-o", "--original-image",
                    required=True,
                    help="The original image src for user")
parser.add_argument("-u", "--unknown-image",
                    required=True,
                    help="The unknown image src")
args = parser.parse_args()

original_image_src = args.original_image
unknown_image_src = args.unknown_image

original_image = face_recognition.load_image_file(original_image_src)
original_image_face_encoding = face_recognition.face_encodings(original_image)[
    0]

unknown_picture = face_recognition.load_image_file(unknown_image_src)
unknown_face_encoding = face_recognition.face_encodings(unknown_picture)[0]

results = face_recognition.compare_faces(
    [original_image_face_encoding], unknown_face_encoding)

data = {
    "is_same_user": results[0] == True
}
print(data)
