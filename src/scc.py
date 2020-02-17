import os
import config
from flask import Flask, flash, request, redirect, url_for, render_template, send_from_directory
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = '../uploads/'
# ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
ALLOWED_EXTENSIONS = {'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.errorhandler(404)


@app.route('/')
def index():
    return render_template('index.html', email=config.email)


@app.route('/about/')
def about():
    return render_template('about.html', email=config.email)


@app.route('/classify/', methods=['GET', 'POST'])
def classify():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            # filename = secure_filename(file.filename)
            # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('results',
                                    filename=file.filename))
    return render_template('classify.html', email=config.email)


@app.route('/results/<filename>')
def results(filename):
    return render_template('results.html', email=config.email)
    
    #send_from_directory(app.config['UPLOAD_FOLDER'],
    #                           filename)


@app.route('/links/')
def links():
    return render_template('links.html', email=config.email)


def not_found(e):
  return render_template('404.html', email=config.email)
