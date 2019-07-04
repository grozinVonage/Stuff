#!/usr/bin/python

import os.path
import threading


from flask import Flask, render_template, Response, request , jsonify

import webview
import sys
import mythread


# =========================================================

app = Flask(__name__)
#app._static_folder = os.path.abspath("templates/static/")
# app.config.from_object(__name__)

#app.secret_key = 's3cr3t'
#app.debug = True


stopFlag = None
myThread = None

# =========================================================
@app.route('/', methods=['GET'])
def index(file_name = 'index.html'):
    return render_template(file_name)

# =========================================================


@app.route('/stop',methods = ['POST', 'GET'])
def stop():
    global stopFlag
    if request.method == 'POST':
        stopFlag.set()
        myThread.stopped = True
        myThread.do_connect()

        return render_template('index.html')

# =========================================================


@app.route('/run',methods = ['POST','GET'])
def run():
    global myThread
    global stopFlag
    if request.method == 'POST':
        stopFlag = threading.Event()
        myThread = mythread.MyThread(stopFlag)

        result = request.form
        disconnect_interval = result["disconnect"]
        offline_time = result["offline"]
        myThread.set(disconnect_interval,offline_time)
        myThread.start()
        # return render_template('index.html')
        # params = {'offline_time': offline_time}
        # return jsonify(params)
        #return metrics('run.html')
        return 'OK', 200
# =========================================================


def start_server():
   app.run(host='0.0.0.0', port=5000)


# =========================================================
if __name__ == '__main__':

    t = threading.Thread(target=start_server)
    t.daemon = True
    t.start()

    webview.create_window("For Vonage QA", "http://127.0.0.1:5000/")

    sys.exit()


#===========================================================




