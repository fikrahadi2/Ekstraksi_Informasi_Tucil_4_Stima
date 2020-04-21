import os
from os import listdir
from os.path import isfile, join
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import sys
sys.path.insert(0, 'algofiles/')
from algos import *

currDir = os.getcwd() + '/uploads'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = currDir
app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    onlyfiles = [f for f in listdir(currDir) if isfile(join(currDir, f))]
    for el in onlyfiles:
        os.remove(currDir+'/'+el)
    return render_template('index.html')
 
@app.route('/upload', methods=['POST'])
def upload():
    uploaded_files = request.files.getlist("file[]")
    filenames = []
    for file in uploaded_files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            filenames.append(filename)
    return render_template('upload.html', filenames=filenames)

@app.route('/profil')
def profil():
    return render_template('perihal.html')

@app.route('/results', methods=['POST'])
def hasil():
    text = request.form['text']
    option = request.form['inlineRadioOptions']
    kirim=Apps(currDir, text, option)
    package=[kirim, text]
    return render_template('results.html', kirim=package)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],filename)

if __name__ == '__main__':
    app.run()
