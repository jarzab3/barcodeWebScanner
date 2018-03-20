from flask import Flask, render_template, Response, jsonify, request
import settings
import time
# import urllib2
import numpy as np
import cv2
import imutils
import datetime
import base64
import subprocess
from flask import send_file, send_from_directory
import csv
from time import gmtime, strftime


app = Flask(__name__,
            static_url_path='',
            static_folder='static',
            template_folder='templates')


log = settings.logging


@app.route('/')
def index():
    return render_template('dashboard.html')


# For AI pages
@app.route('/getDataSet1')
def getDataSet1():
    return render_template('cw2DataSet1.csv')


@app.route('/getDataSet2')
def getDataSet2():
    return render_template('cw2DataSet2.csv')


# Download example. It is
@app.route('/getDataSet2turnedoff')  # this is a job for GET, not POST
def plot_csv1():
    return send_file('extraFiles/cw2DataSet2.csv',
                     mimetype='text/csv',
                     attachment_filename='cw2DataSet2.csv',
                     as_attachment=True)


@app.route('/viewCV')
def view_resume():
    return render_template('pdfViewer.html')

@app.route('/downloadCV')
def download_resume():
    return send_file('static/other/adam_jarzebak_cv.pdf', mimetype='pdf', as_attachment=True)


def convert_and_save(b64_string):
    str1 = b64_string[22:]

    data = base64.b64decode(str1)

    fileWriter = open("digit/digit.png", "wb")
    fileWriter.write(data)
    fileWriter.close()


def executeDigitRecognitionJava():
    try:
        response = subprocess.check_output("java Main", shell=True, stderr=subprocess.STDOUT, cwd="digit/")
        return response
    except subprocess.CalledProcessError as e:
        raise RuntimeError("Command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.output))
        #     return "Error while trying to recognize digit. Please try later."


@app.route('/dashboard')
def govDataAccess():


    results = "No changes found"

    import math

    # print (dataFromFile)
    # print (len(dataFromFile), len(newUrls))

    print(DeepDiff(dataFromFile, newUrls))

    if not (len(dataFromFile) == len(newUrls)):
        results = "Found change for {}. Missing {} file".format(page[0], math.fabs(len(dataFromFile) - len(newUrls)))

    return render_template('dashboard.html', text=results)


@app.route('/apiImage')
def ai_query_image():
    f = request.args.get('image')

    convert_and_save(f)

    log.info("Digit received from web. Start processing!")

    prediction = executeDigitRecognitionJava()

    log.info("Java executed. Predicted digit: {}".format(prediction))

    log.debug("Address: {}".format(request.remote_addr))

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
    app.run(host='0.0.0.0', port=443, threaded=True, ssl_context=('/etc/letsencrypt/live/adam.sobmonitor.org/fullchain.pem','/etc/letsencrypt/live/adam.sobmonitor.org/privkey.pem'))
    # app.run(host='0.0.0.0', port=443, threaded=True, ssl_context=context)
    log.debug("Started up barcode app")
