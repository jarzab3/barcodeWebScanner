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
<<<<<<< HEAD
from flask_analytics import Analytics
from OpenSSL import SSL
=======
import csv
from time import gmtime, strftime
>>>>>>> 3ef34b191226f983ab31e4b62d2e5fc59fba7636

from deepdiff import DeepDiff
from pprint import pprint

from Utils.writeToTSV import *
from convertToTSV import *

from getFilesFromWebsite import checkForUpdate, getLinksFromPage, clearDir

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

    basePath = 'dataFiles/'

    # Setup stats file
    statsPath = "stats/general.tsv"

    # clearDir("stats/")

    # Construct stats headers
    headersData = ["local_authority_name", "base_url", "data_url", "file_type", "parent_container_element", "attr_type",
                   "attr_name", "is_direct_access", "urls", "last_update"]

    # writeToCSV(statsPath, headersData)

    last_update = strftime("%Y-%m-%d %H:%M:%S", gmtime())

    page1 = ["ashfield", "https://www.ashfield.gov.uk", "https://www.ashfield.gov.uk/your-council/public-data/finances/payments-to-suppliers/", "csv", ["div", "class", "col-md-6 column"], False]

    page = page1

    # Initial file getting
    # urls = getLinksFromPage(page[0], page[1],page[2], page[3], page[4], page[5])
    # update stats file

    # statsRow = [page[0], page[1],page[2], page[3], page[4], page[5], last_update, urls]



    # writeToCSV(statsPath, statsRow)

    # Convert data to tsv file
    # writetoTSV(page[0])

    # Check for an update

    newUrls = checkForUpdate(page[0], page[1],page[2], page[3], page[4], page[5])

    # print(newUrls)

    statsPath = "stats/general.tsv"

    header = []

    rowCounter = 0

    dataToCompare = []

    with open(statsPath, 'r') as tsvfile:
        reader = csv.reader(tsvfile, delimiter='\t')
        header = False

        for i, row in enumerate(reader):
            if header == False:
                header = row
                header = True
            else:
                dataToCompare = row[7]

                # print(row[7])
                rowCounter += 1


    dataFromFile = []

    dataToCompare = dataToCompare.replace("[", "").replace("]", "")
    text = dataToCompare.split(',')

    for i in text:
        i = i.replace("'", "").replace(" ", "")
        dataFromFile.append(i)
        # print (i)

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



context = SSL.Context(SSL.SSLv23_METHOD)
context.use_privatekey_file('/etc/letsencrypt/live/adam.sobmonitor.org/privkey.pem')
context.use_certificate_file('/etc/letsencrypt/live/adam.sobmonitor.org/fullchain.pem')


if __name__ == '__main__':
<<<<<<< HEAD
    # app.run(host='0.0.0.0', port=443, threaded=True, ssl_context=('/etc/letsencrypt/live/adam.sobmonitor.org/fullchain.pem','/etc/letsencrypt/live/adam.sobmonitor.org/privkey.pem'))
    app.run(host='0.0.0.0', port=443, threaded=True, ssl_context=context)
    log.debug("Started up analysis app")
=======
    app.run(host='0.0.0.0', port=8000, threaded=True, debug=True)
    log.debug("Started up dashboard app")
>>>>>>> 3ef34b191226f983ab31e4b62d2e5fc59fba7636
