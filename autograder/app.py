from flask import Flask, request, Response, send_file
import json
import zipfile
import os
import unittest
import subprocess
from gradescope_utils.autograder_utils.json_test_runner import JSONTestRunner
from io import BytesIO

app = Flask(__name__)

def check_auth(username, password):
    return username == os.environ.get('USERNAME') and password == os.environ.get('PASSWORD')

def authenticate():
    return Response(
        'Could not verify your access level for that URL.\n'
        'You have to login with proper credentials', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})

@app.route('/', methods=['POST'])
def upload_file():
    auth = request.authorization
    if not auth or not check_auth(auth.username, auth.password):
        return authenticate()

    if 'submission.zip' not in request.files:
        return 'No file part', 400

    file = request.files['submission.zip']
    if file.filename == '':
        return 'No selected file', 400

    if file:
        if os.path.isfile('/app/calculator.py'):
            os.remove('/app/calculator.py')
        if os.path.isfile('/app/results.json'):
            os.remove('/app/results.json')

        # Unzip the file and run tests
        with zipfile.ZipFile(file, 'r') as zip_ref:
            zip_ref.extractall('/app/')

        subprocess.run(['python', 'run_tests.py'])
        # Send back results.json
        return send_file('/app/results.json')
    else:
        return 'File not found', 400

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)),ssl_context='adhoc')

