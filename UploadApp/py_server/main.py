#!/usr/bin/env python

"""Extend Python's built in HTTP server to save files

curl or wget can be used to send files with options similar to the following

  curl -X PUT --upload-file somefile.txt http://localhost:8000
  wget -O- --method=PUT --body-file=somefile.txt http://localhost:8000/somefile.txt

__Note__: curl automatically appends the filename onto the end of the URL so
the path can be omitted.

"""
import base64
import os
import json

from requests import Response

try:
    import http.server as server
except ImportError:
    # Handle Python 2.x
    import SimpleHTTPServer as server

class HTTPRequestHandler(server.SimpleHTTPRequestHandler):
    myJSON = {'alon':'yep'}
    """Extend SimpleHTTPRequestHandler to handle PUT requests"""
    def do_PUT(self):
        """Save a file following a HTTP PUT request"""
        print(self.path)
        filename = os.path.basename(self.path)

        # Don't overwrite files
        if os.path.exists(filename):
            self.send_response(409, 'Conflict')
            self.end_headers()
            #reply_body = '"%s" already exists\n' % filename
            #self.wfile.write(reply_body.encode('utf-8'))
            ret_json = {}
            ret_json['file'] = filename
            ret_json['Conflict'] = "already exists"
            json_data = json.dumps(ret_json)
            resp = Response(json_data, status=409, mimetype='application/json')

            self.send_response(resp)
            self.end_headers()
            return

        file_length = int(self.headers['Content-Length'])
        with open(filename, 'wb') as output_file:
            # output_file.write(base64.decode(self.rfile.read(file_length)))
            #s = self.rfile.read(file_length)
            #print(s)
            # data = base64.b64decode(s)
            output_file.write(self.rfile.read(file_length))

        ret_json = {}
        ret_json['file'] = filename
        json_data = json.dumps(ret_json)
        resp = Response(json_data, status=200, mimetype='application/json')

        # st = json.loads(self.json_data)
        #byt = json_data.encode()
        #self.wfile.write(ret_json)
        #reply_body = 'Saved "%s"\n' % filename
        #self.wfile.write(reply_body.encode('utf-8'))
        #self.send_response(201, 'Created')
        self.send_response(resp)
        self.end_headers()

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        # Send the html message
        st = json.loads(self.myJSON)
        byt = st.encode()
        self.wfile.write(byt)
        return

if __name__ == '__main__':
    server.test(HandlerClass=HTTPRequestHandler)