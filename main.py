import face_recognition
import argparse
import requests
import re
import os
import imghdr
from time import gmtime, strftime

parser = argparse.ArgumentParser(
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-o", "--original-image",
                    required=True,
                    help="The original image src for user")
parser.add_argument("-u", "--unknown-image",
                    required=True,
                    help="The unknown image src")
args = parser.parse_args()


def main():
    original_image_src = download_image(args.original_image)
    unknown_image_src = download_image(args.unknown_image)

    original_image = face_recognition.load_image_file(original_image_src)
    original_image_face_encoding = face_recognition.face_encodings(original_image)[
        0]

    unknown_picture = face_recognition.load_image_file(unknown_image_src)
    unknown_face_encoding = face_recognition.face_encodings(unknown_picture)[0]

    results = face_recognition.compare_faces(
        [original_image_face_encoding],
        unknown_face_encoding,
    )

    remove_image(original_image_src)
    remove_image(unknown_image_src)

    data = {
        "is_same_user": results[0] == True
    }
    print(data)


def check_for_image(response):
    if 'image' in response.headers['Content-Type']:
        # Using imghdr module to verify the signature of the image
        image_type = imghdr.what('', response.content)
        if image_type:
            print("Image type detected: {0}".format(image_type))
            return True
        else:
            print("Error: Unable to verify the signature of the image")
            exit(1)
    return False


def download_image(url):
    try:
        response = requests.get(url)
    except:
        print("Error: While requesting url: {0}".format(url))
        exit(1)

    if response:
        if check_for_image(response):
            extension = os.path.basename(response.headers['Content-Type'])
            if 'content-disposition' in response.headers:
                content_disposition = response.headers['content-disposition']
                filename = re.findall("filename=(.+)", content_disposition)
            elif url[-4:] in ['.jpg', 'jpeg']:
                filename = os.path.basename(url)
            else:
                filename = 'image_{0}{1}'.format(
                    strftime("%Y%m%d_%H_%M_%S", gmtime()), '.' + str(extension))

            path = f"temp/{filename}"
            with open(path, 'wb+') as wobj:
                wobj.write(response.content)
            return path
        else:
            print("Sorry: The url doesn't contain any image :(")
            exit(1)


def remove_image(path):
    if os.path.isfile(path):
        os.remove(path)
        print("File has been deleted")
    else:
        print("File does not exist")


main()
