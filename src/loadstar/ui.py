#Import necessary libraries
from flask import Flask, render_template, Response, send_file, jsonify, make_response
import io
import cv2

# create the Flask app
app = Flask(__name__, template_folder='web', static_url_path="/static", static_folder='web_static')

ds = None

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/stats.json')
def stats():
	return jsonify({
		'fps': ds['fps'],
		'loading': ds['loading'],
		'capturing': ds['capturing'],
		'frameInterval': ds['frameInterval'],
		'loadingColour': ds['loadingColour']
	})

@app.route('/log.json')
def logJSON():
	return jsonify(ds['log'].output_dict)

@app.route('/log.txt')
def logTXT():
		response = make_response(str(ds['log']), 200)
		response.mimetype = "text/plain"
		return response

@app.route('/log.html')
def logHTML():
	return ds['log'].html

@app.route('/video')
def video():
	return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

def gen():
	while True:
		ret, jpeg = cv2.imencode('.jpg', ds['frame'])
		frame = jpeg.tobytes()
		yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def start(d):
	global ds
	ds = d
	app.config['TEMPLATES_AUTO_RELOAD'] = True
	app.run()

if __name__ == '__main__':
	start()