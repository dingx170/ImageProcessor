from flask import Flask, request
import numpy as np
from cv2 import cv2
import json

# Initialize the Flask application
app = Flask(__name__)


@app.route('/process', methods=['POST'])
def process():
    image = request.data
    params = request.args

    actions = [param for param in params]
    actions = json.loads(actions[0])

    # convert image from string to uint8
    nparr = np.fromstring(image, np.uint8)
    # decode image
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    for action in actions:

        if action['action'] == 'flip_H':
            img = cv2.flip(img, 0)
            continue

        elif action['action'] == 'flip_V':
            img = cv2.flip(img, 1)
            continue

        elif action['action'] == 'rotate_R':
            img = rotateImage(img, -90)
            continue

        elif action['action'] == 'rotate_L':
            img = rotateImage(img, 90)
            continue

        elif action['action'] == 'rotate':
            img = rotateImage(img, int(action['param']))
            continue

        elif action['action'] == 'resize':
            img = resizeImage(int(action['param']), img)
            continue

        elif action['action'] == 'thumbnail':
            img = resizeImage(10, img)
            continue

        elif action['action'] == 'grayscale':
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            continue

    _, img_encoded = cv2.imencode('.jpeg', img)

    return img_encoded.tostring(), 200

def resizeImage(pct, img):
    width = int(img.shape[1] * pct / 100)
    height = int(img.shape[0] * pct / 100)
    return cv2.resize(img, (width, height))

def rotateImage(image, angle):
    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
    result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
    return result

# start flask app
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)