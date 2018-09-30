from flask import Flask, render_template, send_from_directory, request, redirect
import glob
import os
import csv

IMAGES_DIRECTORY = 'images'
OUTPUT_FILE = 'tagging.csv'

app = Flask(__name__)

@app.route('/tag', methods=["POST"])
def tag():
    image = request.form["image"]
    count = request.form["count"]
    set_image_tag(image, count)
    images = get_images(IMAGES_DIRECTORY)
    return redirect('/')

@app.route('/', methods=["GET"])
def index():
    images = get_images(IMAGES_DIRECTORY)
    images_untagged = [image for image in images if image not in get_tagged_images()]
    image_path = None if len(images_untagged) == 0 else images_untagged[0]
    if image_path is None:
        return render_template("tag.html", images_left = 0)
    else:
        images_left = len(images_untagged)
        return render_template("tag.html", image = image_path, images_left = images_left)

@app.route('/{}/<path:path>'.format(IMAGES_DIRECTORY))
def image(path):
    relative_image_dir = './{}'.format(IMAGES_DIRECTORY)
    return send_from_directory(relative_image_dir, path)

def get_images(directory):
    return glob.glob(directory + '/*.jpg')

def set_image_tag(image, count):
    if not os.path.isfile(OUTPUT_FILE):
        init_output_file(OUTPUT_FILE)
    with open(OUTPUT_FILE, 'a') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',')
        filewriter.writerow([image, count])

def get_tagged_images():
    if not os.path.isfile(OUTPUT_FILE):
        return {}
    with open(OUTPUT_FILE, 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        return {rows[0]: rows[1] for rows in reader}

def init_output_file(filename):
    with open(OUTPUT_FILE, 'w') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',')
        filewriter.writerow(['Image', 'People Count'])

if __name__ == "__main__":
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True, host='0.0.0.0')
