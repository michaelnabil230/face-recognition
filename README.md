# Face recognition

## Install requirements:

To install the requirements, run the following command:

```bash
pip install -r requirements.txt
```

## How to run as a server?

To run the application as a server, use the following command:

```bash
flask run
```

The Flask API will be hosted on port 5000.

### Endpoints

- /api/compare-faces

## How to run from the command line?

To run the application from the command line, use the following command:

**Note: It is important to replace the arguments with the URLs or file paths of your own images.**

```bash
python3 command_line.py -o=https://example.com/original.jpg -u=https://example.com/unknown.jpg
```

```bash
python3 command_line.py -o=https://cdn.searchenginejournal.com/wp-content/uploads/2022/04/personal-branding-62792f2def4b9-sej-1520x800.png -u=https://thumbs.dreamstime.com/z/personal-branding-26135617.jpg
```

```bash
python3 command_line.py -o=images/king-salman/1.jpeg -u=images/king-salman/2.jpeg
```

```bash
python3 command_line.py -o=images/obama/1.jpeg -u=images/king-salman/2.jpeg
```

## Additional Information

Face recognition is a technology that identifies and verifies individuals by analyzing their facial features. It has various applications, including access control, surveillance systems, and personal identification. This project provides a face recognition system that can be run either as a server or from the command line.

The `/api/compare-faces` endpoint is used to compare two faces and determine if they belong to the same person. It accepts input images and returns a response indicating the similarity between the faces.

To run the application as a server, use the `flask run` command, and the server will be accessible on port 5000. The `/api/compare-faces` endpoint can be accessed by sending a POST request to that URL.

To run the application from the command line, use the `command_line.py` script and provide the URLs or file paths of the images you want to compare as command-line arguments. The script will process the images and provide the result in the console output.