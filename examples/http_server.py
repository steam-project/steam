#!/usr/bin/python3

import os, json, time
from waitress import serve
from flask import Flask, request, jsonify
from datetime import datetime

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

quant = 0
strData = []

app = Flask(__name__)
 
@app.route("/")
def hello():
    dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return "STEAM IoT<br>\nServer datetime: {}".format(dt)
    
@app.route("/save")
def save():
    global quant
    global strData
    fout = open('logdata.txt', 'w')
    fout.write('\n'.join(strData))
    fout.close()
    strData.clear()
    quant = 0

    dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print('\rFile saved and memory clear: {}'.format(dt))
    return "STEAM IoT<br>\nFile saved and memory clear: {}".format(dt)

@app.route("/wso2", methods=['POST', 'GET'])
def wso2():
    global quant
    global strData
    quant += 1
    data = request.data.decode()
    data = data.replace('\n', ' ')
    while data.find('  ') >= 0:
        data = data.replace('  ', ' ')
    strData.append(data)
    print('\r{}'.format(quant), end='')
    return 'OK'

if __name__ == "__main__":
    serve(app, threads=128, listen='*:8080')
