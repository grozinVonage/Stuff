#!flask/bin/python
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, World!"



@app.route('/handle_form', methods=['POST'])
def handle_form():
    print("Posted file: {}".format(request.files['file']))
    file = request.files['file']
    return ""

@app.route('/<string:file_name>', methods = ['PUT'])
def upload_file(file_name):
    with open(file_name, 'wb') as output_file:
        output_file.write(request.stream.read())
    return jsonify({'file': file_name})

if __name__ == '__main__':
    app.debug = True
    app.run(host='192.168.1.104', port=8000)
