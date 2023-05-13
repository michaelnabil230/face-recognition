# Face recognition

## Install requirements:

To install the requirements

```bash
pip install -r requirements.txt
```

## How to run as serve ?

```bash
flask run
```

Flask api will be hosted 5000 port
### Endpoints
- /api/compare-faces 

## How to run as command line ?

To run the app with this command line 

**Note**: Very important change the arguments with your images for you

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