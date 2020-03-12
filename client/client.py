from flask import Flask, render_template, request, jsonify
import requests
# import jsonify
import numpy as np
from cv2 import cv2

addr = 'http://localhost:5001'

process_url = addr + '/process'

app = Flask(__name__)

@app.route('/')
def home():
	return render_template('index.html', oriImg=None, newImg=None, actions=None)

@app.route('/process', methods=['POST', 'GET'])
def process_image():
	image = request.form['file']
	actions = request.form['action']
	output_name = "static/media/output.jpg"
	send_request(process_url, image, actions, output_name)

	return jsonify({'image_url': output_name})


def send_request(url, image, actions, outputname):
	# prepare headers for http request
	content_type = 'image/jpeg'
	headers = {'content-type': content_type}

	img = cv2.imread(image)

	# encode image as jpeg
	_, img_encoded = cv2.imencode('.jpeg', img)

	# send http request with image and receive response
	response = requests.post(url, data=img_encoded.tostring(), params=actions, headers=headers)

	# convert content of response data to uint8
	nparr = np.fromstring(response.content, np.uint8)
	# # decode image
	img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

	cv2.imwrite(outputname, img)


if __name__ == '__main__':
	app.run(debug=True)