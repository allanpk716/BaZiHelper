# -*- coding: utf-8 -*-
import os
from flask import Flask, render_template, request
from flask import jsonify
import BaZiHelper

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/calcBaZi', methods=['POST'])
def calcBaZi():
    pickdate = request.form['pickdate']
    picktime = request.form['picktime']
    latit = request.form['latit']
    longit = request.form['longit']
    ipadd = request.form['ipadd']
    timezone = request.form['timezone']
    countryCode = request.form['countryCode']

    solarTime, strBaZi, shuxing = BaZiHelper.Calc(pickdate, picktime, latit, longit, ipadd, timezone, countryCode)
    d = {'strBaZi': strBaZi, 'solarTime': solarTime.strftime('%Y-%m-%d %H:%M:%S'), "shuxing": shuxing }
    return jsonify(d)

if __name__ == '__main__':
    app.run(debug=True, port=8181)