from flask import Flask, request
import numpy as np
from cv2 import cv2

# Initialize the Flask application
app = Flask(__name__)


@app.route('/flip', methods=['POST'])
def flip():	
    direction = request.args.get('direction')
    # convert image from string to uint8
    nparr = np.fromstring(request.data, np.uint8)
    # decode image
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    # flip image
    output = ''
    if direction == 'H':
        output = cv2.flip(img, 1)
    elif direction == 'V':
        output = cv2.flip(img, 0)

    _, img_encoded = cv2.imencode('.jpeg', output)

    return img_encoded.tostring(), 200



@app.route('/rotateCW', methods=['POST'])
def rotateCW():	
    angle = request.args.get('angle')
    nparr = np.fromstring(request.data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)   
    output = rotateImage(img, int('-' + angle))
    _, img_encoded = cv2.imencode('.jpeg', output)

    return img_encoded.tostring(), 200

@app.route('/rotateCCW', methods=['POST'])
def rotateCCW():	
    angle = request.args.get('angle')
    nparr = np.fromstring(request.data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)   
    output = rotateImage(img, int(angle))
    _, img_encoded = cv2.imencode('.jpeg', output)

    return img_encoded.tostring(), 200



def rotateImage(image, angle):
    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
    result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
    return result

# start flask app
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)