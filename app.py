from flask import Flask, render_template, Response, jsonify, request
import settings
import time
# import urllib2
import numpy as np
import cv2
import datetime
import base64
import subprocess
from flask import send_file, send_from_directory
from time import gmtime, strftime
from flask import Flask,redirect
import json
# Barcode recognition
from pyzbar.pyzbar import decode
from PIL import Image


app = Flask(__name__,
            static_url_path='',
            static_folder='static',
            template_folder='templates')


log = settings.logging

@app.before_request
def before_request():
    if request.url.startswith('http://'):
        url = request.url.replace('http://', 'https://', 1)
        code = 301
        return redirect(url, code=code)


@app.route('/')
def index():
    return render_template('dashboard.html')


@app.route('/camera')
def cameraTest():
    return render_template('camera-test.html')


python_data = {
    'some_list': [4, 5, 6],
    'nested_dict': {'foo': 7, 'bar': 'a string'}
}


@app.route('/lope')
def testCam():
    # events = api.call(get_event, arg0, arg1)
    # geocode = event['latitude'], event['longitude']

    obj = { 'hello': 'world' }

    # geocode = json.dumps("val1", "val2")
    geocode = json.dumps("image2", "1")

    return render_template('images.html', value=geocode)

    # books = {
    #     "Learn Python The Hard Way": {
    #         "author": "Shaw, Zed",
    #         "rating": "3.92",
    #         "image": "ef0ceaab-32a8-47fb-ba13-c0b362d970da.jpg"
    #     }
    # }

    # passing data to the template
    # return render_template("iamges.htm", books=books)


    # return render_template('images.html')






def convert_and_save(b64_string):
    str1 = b64_string[22:]

    data = base64.b64decode(str1)

    fileWriter = open("barcodeImage/image.jpg", "wb")
    fileWriter.write(data)
    fileWriter.close()


def executeBarcodeRecognition():
    try:
        log.debug(decode(Image.open('barcodeImage/image.jpg')))
    except Exception as error:
        log.error("Could not decode this image")


@app.route('/apiImage')
def ai_query_image():

    f = request.args.get('image')

    convert_and_save(f)

    log.info("Digit received from web. Start processing!")

    prediction = executeBarcodeRecognition()

    print (prediction)
    # log.debug("Address: {}".format(request.remote_addr))

    return jsonify(result=prediction)



@app.route('/_apiQuery')
def api_query_task():
    query = request.args.get('apiQ0', "", type=str).strip()

    color = True

    reply = ""

    if query == "color":
        color = True
        reply = "Changed to color"
    elif query == "gray":
        color = False
        reply = "Changed to gray"

    return jsonify(result=reply)


# context = SSL.Context(SSL.SSLv23_METHOD)
# context.use_privatekey_file('/etc/letsencrypt/live/adam.sobmonitor.org/privkey.pem')
# context.use_certificate_file('/etc/letsencrypt/live/adam.sobmonitor.org/fullchain.pem')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=443, threaded=True, debug=True, ssl_context=('/etc/letsencrypt/live/adam.sobmonitor.org/fullchain.pem','/etc/letsencrypt/live/adam.sobmonitor.org/privkey.pem'))
    # app.run(host='0.0.0.0', port=443, threaded=True, ssl_context=context)
    log.debug("Started up barcode app")
