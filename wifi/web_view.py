#!/usr/bin/python
import os
import os.path
import time

from flask import Flask, render_template, Response

import webview
import sys
import threading


# =========================================================


def do_connect():
    os.system("networksetup -setairportpower airport on")
    print("Connected : %s" % time.ctime())


# =========================================================


def do_disconnect():
    os.system("networksetup -setairportpower airport off")
    print("Disconnected : %s" % time.ctime())


# =========================================================
app = Flask(__name__)
app.config.from_object(__name__)
# =========================================================

def root_dir():  # pragma: no cover
    return os.path.abspath(os.path.dirname(__file__))

# =========================================================
def get_file(filename):  # pragma: no cover
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
def metrics():  # pragma: no cover
    content = get_file('index.html')
    return Response(content, mimetype="text/html")

# =========================================================
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def get_resource(path):  # pragma: no cover
    mimetypes = {
        ".css": "text/css",
        ".html": "text/html",
        ".js": "application/javascript",
    }
    complete_path = os.path.join(root_dir(), path)
    ext = os.path.splitext(path)[1]
    mimetype = mimetypes.get(ext, "text/html")
    content = get_file(complete_path)
    return Response(content, mimetype=mimetype)
    #return render_template('index.html',**locals())

# =========================================================


def start_server():
   #app.run()
   app.run(host='0.0.0.0', port=5000)

# =========================================================


if __name__ == '__main__':
    """  https://github.com/r0x0r/pywebview/blob/master/examples/http_server.py
    """

    t = threading.Thread(target=start_server)
    t.daemon = True
    t.start()

    webview.create_window("For Vonage QA", "http://127.0.0.1:5000/")

    sys.exit()


#===========================================================




