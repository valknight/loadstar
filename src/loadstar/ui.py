#Import necessary libraries
from flask import Flask, render_template, Response, send_file, jsonify
import io
import cv2

#Initialize the Flask app
app = Flask(__name__, template_folder='web')

ds = None

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/stats')
def stats():
	return jsonify({
		'fps': ds['fps'],
		'loading': ds['loading'],
		'capturing': ds['capturing']
	})

@app.route('/log')
def log():
	return jsonify(ds['log'].output_dict)


@app.route('/video')
def video():
	return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

def gen():
	while True:
		print(ds['frame'])
		ret, jpeg = cv2.imencode('.jpg', ds['frame'])
		frame = jpeg.tobytes()
		yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def start(d):
	global ds
	ds = d
	app.run()

if __name__ == '__main__':
	start()