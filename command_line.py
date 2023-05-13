from deepface import DeepFace
import argparse
import requests
import re
import os
import imghdr
from time import gmtime, strftime

parser = argparse.ArgumentParser(
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)
parser.add_argument(
    "-o",
    "--original-image",
    required=True,
    help="The original image source for the user",
)
parser.add_argument(
    "-u",
    "--unknown-image",
    required=True,
    help="The unknown image source",
)
args = parser.parse_args()


def main():
    original_image_src, unknown_image_src = get_images()

    try:
        is_same_user = DeepFace.verify(
            original_image_src,
            unknown_image_src,
        )['verified']
    except ValueError:
        print('Error')
        is_same_user = False

    remove_image(original_image_src)
    remove_image(unknown_image_src)

    print({
        "is_same_user": bool(is_same_user)
    })


def is_valid_url(url):
    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or IP
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    return re.match(regex, url) is not None


def get_images():
    if is_valid_url(args.original_image):
        original_image_src = download_image(args.original_image)
    else:
        original_image_src = args.original_image

    if is_valid_url(args.unknown_image):
        unknown_image_src = download_image(args.unknown_image)
    else:
        unknown_image_src = args.unknown_image

    return [original_image_src, unknown_image_src]


def check_content_type(response):
    if 'image' in response.headers['Content-Type']:
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
        print("Error: While requesting URL: {0}".format(url))
        exit(1)

    if response:
        if check_content_type(response):
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
            with open(path, 'wb+') as file_obj:
                file_obj.write(response.content)
            return path
        else:
            print("Sorry: The URL doesn't contain any image :(")
            exit(1)


def remove_image(path):
    if os.path.isfile(path):
        os.remove(path)
        print("File has been deleted")


if __name__ == "__main__":
    main()
