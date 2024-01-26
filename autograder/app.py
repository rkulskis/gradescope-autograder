from flask import Flask, request, Response, send_file
import zipfile
import os
import subprocess
import threading
import sys

lock = threading.Lock()

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
        print(f"{threading.current_thread().name} waiting on LOCK", file=sys.stderr)
        with lock:
            # Unzip the file and run tests
            print(f"GOT LOCK {threading.current_thread().name}", file=sys.stderr)
            with zipfile.ZipFile(file, 'r') as zip_ref:
                zip_ref.extractall('/app/')

            subprocess.run(['python', 'run_tests.py'])
    
            return send_file('/app/results.json')
    else:
        return 'File not found', 400

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)),ssl_context='adhoc')
