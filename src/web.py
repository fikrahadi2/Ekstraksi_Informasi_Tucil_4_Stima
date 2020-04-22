import os
import sys

from os import listdir
from os.path import isfile, join
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
from main import *

upDir = os.getcwd() + '/upload'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = upDir
app.config['ALLOWED_EXTENSIONS'] = set(['txt'])

def openFile(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    files = [f for f in listdir(upDir) if isfile(join(upDir, f))]
    for f in files:
        os.remove(upDir+'/'+f)
    return render_template('index.html')
 
@app.route('/upload', methods=['POST'])
def upload():
    uploaded_files = request.files.getlist("file[]")
    nama_file = []
    for file in uploaded_files:
        if file and openFile(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            nama_file.append(filename)
    return render_template('upload.html', nama_file=nama_file)

@app.route('/upload/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],filename)
    
@app.route('/perihal')
def perihal():
    return render_template('perihal.html')

@app.route('/hasil', methods=['POST'])
def hasil():
    pattern = request.form['pattern']
    opsi = request.form['inlineRadioOptions']
    send = openApp(upDir, pattern, opsi)
    package = [send, pattern]
    return render_template('hasil.html', send=package)

if __name__ == '__main__':
    app.run()
