# Import necessary libraries
import json
from re import T
from flask import Flask, render_template, Response, send_file, jsonify, make_response
import threading
import webbrowser
import time
import os
import io
import cv2
import logging
import asyncio
import sys

lastFrame = None
lastFrameTime = 0
if getattr(sys, 'frozen', False):
    templatesDir = os.getcwd() + '/web'
    staticDir = os.getcwd() + '/web_static'
else:
    templatesDir = 'web'
    staticDir = 'web_static'

# create the Flask app
app = Flask(__name__, template_folder=templatesDir, static_folder=staticDir, static_url_path="/static")

ds = None


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/stats.json')
def stats():
    try:
        return jsonify({
            'fps': ds['fps'],
            'loading': ds['loading'],
            'capturing': ds['capturing'],
            'frameInterval': ds['frameInterval'],
            'loadingColour': ds['loadingColour'],
            'queuedAction': ds.get('action'),
            'starting': False
        })
    except KeyError:
        return jsonify({
            'starting': True
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


@app.route('/action/<actionCommand>')
def actionRoute(actionCommand):
    action(actionCommand)
    sys.exit(0)
    return "OK", 200


def gen():
    global lastFrame
    global lastFrameTime
    while True:
        # This caps us to only only encode at a max of 24FPS, reducing CPU usage especially with multiple pages open
        if time.time() - lastFrameTime > (1/24):
            ret, jpeg = cv2.imencode('.jpg', ds['frame'])
            lastFrame = jpeg.tobytes()
            lastFrameTime = time.time()
            yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + lastFrame + b'\r\n\r\n')
        else:
            time.sleep(1/24)


def action(actionCommand: str):
    ds['action'] = actionCommand


def start(d):
    global ds
    ds = d
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.WARNING)
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(port=10000)


if __name__ == '__main__':
    start()
