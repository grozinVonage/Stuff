#!/usr/bin/python
import os
import os.path
import time

from flask import Flask, render_template, Response, request

import webview
import sys
import threading


# =========================================================


class MyThread(threading.Thread):

    def __init__(self, event):
        threading.Thread.__init__(self)
        self.stop_event = event
        self.disconnect_interval = 0
        self.offline_time = 0

    def set(self, _disconnect_interval, _offline_time ):
        self.disconnect_interval = int(_disconnect_interval)
        self.offline_time = int(_offline_time)

    def stop(self):
        self.stopped = True

    def run(self):
        while not self.stop_event.wait(self.disconnect_interval):
            print("my thread")
            self.do_disconnect()
            time.sleep(self.offline_time)
            self.do_connect()

    # =========================================================


    def do_connect(self):
        os.system("networksetup -setairportpower airport on")
        print("Connected : %s" % time.ctime())

    # =========================================================

    def do_disconnect(self):
        os.system("networksetup -setairportpower airport off")
        print("Disconnected : %s" % time.ctime())


# =========================================================

app = Flask(__name__)
app.config.from_object(__name__)
stopFlag = None
myThread = None


# =========================================================
def root_dir():
    return os.path.abspath(os.path.dirname(__file__))

# =========================================================


def get_file(filename):
    try:
        src = os.path.join(root_dir(), filename)
        # Figure out how flask returns static files
        # Tried:
        # - render_template
        # - send_file
        # This should not be so non-obvious
        return open(src).read()
    except IOError as exc:
        return str(exc)

# =========================================================


@app.route('/', methods=['GET'])
def metrics(file_name = 'index.html' ):  # pragma: no cover
    content = get_file(file_name)
    return Response(content, mimetype="text/html")

# =========================================================


@app.route('/stop',methods = ['POST', 'GET'])
def stop():
    global stopFlag
    if request.method == 'POST':
        stopFlag.set()
        myThread.stopped = True
        myThread.do_connect()


        return metrics('index.html')

# =========================================================


@app.route('/run',methods = ['POST', 'GET'])
def run():
    global myThread
    global stopFlag
    if request.method == 'POST':
        stopFlag = threading.Event()
        myThread = MyThread(stopFlag)

        result = request.form
        disconnect_interval = result["disconnect"]
        offline_time = result["offline"]
        myThread.set(disconnect_interval,offline_time)
        myThread.start()

        return metrics('run.html')
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




