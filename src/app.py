import cv2, os, threading, time
import numpy as np
from flask import Flask, Response, flash, request, redirect, url_for, render_template, send_from_directory, Response
from werkzeug.utils import secure_filename
from keras.models import load_model
from keras.preprocessing import image

import classes
import config #as config 
import utils #as utils
#import model.label_image as model
#import model.classes as classes



'''if __name__ == '__main__':
    import config as config 
    import utils as utils
    import model.label_image as model
    import model.classes as classes
else:
    import src.config as config
    import src.utils as utils
    import src.model.label_image as model
    import src.model.classes as classes'''


# GStreamer Pipeline to access the Raspberry Pi camera width=3280, height=2464
GSTREAMER_PIPELINE = 'nvarguscamerasrc ! video/x-raw(memory:NVMM), width=299, height=299, format=(string)NV12, framerate=21/1 ! nvvidconv flip-method=0 ! video/x-raw, width=960, height=616, format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink wait-on-eos=false max-buffers=1 drop=True'

# Image frame sent to the Flask object
global video_frame
video_frame = None

UPLOAD_FOLDER = config.uploads
STATIC_FOLDER = './static/'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}

app = Flask(__name__)
app.config['STATIC_FOLDER'] = STATIC_FOLDER
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


def captureFrames():
    global video_frame, thread_lock

    # Video capturing from OpenCV
    video_capture = cv2.VideoCapture(GSTREAMER_PIPELINE, cv2.CAP_GSTREAMER)

    while True and video_capture.isOpened():
        return_key, frame = video_capture.read()
        if not return_key:
            break

        # Create a copy of the frame and store it in the global variable,
        # with thread safe access
        with thread_lock:
            video_frame = frame.copy()

        key = cv2.waitKey(30) & 0xff
        if key == 27:
            break

    video_capture.release()


def encodeFrame():
    global thread_lock
    while True:
        # Acquire thread_lock to access the global video_frame object
        with thread_lock:
            global video_frame
            if video_frame is None:
                continue
            return_key, encoded_image = cv2.imencode(".jpg", video_frame)
            if not return_key:
                continue

            # Output image as a byte array
            yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
                bytearray(encoded_image) + b'\r\n')


def saveFrame():
    #global thread_lock
    with thread_lock:
        global video_frame
        if video_frame is None:
            pass
        return_key, encoded_image = cv2.imencode(".jpg", video_frame)
        if not return_key:
            pass

        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
                bytearray(encoded_image) + b'\r\n')


#@app.errorhandler(404)


@app.route('/')
def index():
    return render_template('index.html', email=config.email, github=config.github)


@app.route('/about/')
def about():
    return render_template('about.html', email=config.email, github=config.github)


#@app.route('/video_feed/')
#def video_feed():
#    return Response(encodeFrame(), mimetype="multipart/x-mixed-replace; boundary=frame")


@app.route('/classify/', methods=['GET', 'POST'])
def classify():
    if request.method == 'POST':
        option = request.form.getlist('options') 
        if option == 'camera':
            return render_template('404.html', email=config.email, github=config.github)
        else:
            #flash('file selected')
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
            if file and utils.allowed_file(file.filename, ALLOWED_EXTENSIONS):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                return redirect(url_for('results',
                                        filename=file.filename))
    return render_template('classify.html', email=config.email, github=config.github)


@app.route('/results/<filename>')
def results(filename):
    #load model
    model_path = os.path.join(app.config['STATIC_FOLDER'], 'model.h5')
    model = load_model(model_path)

    # image path
    img_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    # load a single image
    img = image.load_img(img_path, target_size=(299, 299))
    img = image.img_to_array(img)
    img = np.expand_dims(img, axis=0)

    # check prediction
    pred = model.predict(img)

    #duration, results = model.predict(url_for('uploads', filename=filename))
    results = utils.addClassNames(classes.classNames, pred)
    
    return render_template('results.html', filename=filename, results=results, email=config.email, github=config.github)
    

@app.route('/uploads/<path:filename>')
def uploads(filename):
    return send_from_directory(app.root_path + '/' + config.uploads, filename)


@app.route('/links/')
def links():
    return render_template('links.html', email=config.email, github=config.github)


def not_found(e):
  return render_template('404.html', email=config.email, github=config.github)


if __name__ == '__main__':
    # Create a thread and attach the method that captures the image frames, to it
    #process_thread = threading.Thread(target=captureFrames)
    #process_thread.daemon = True

    # Start the thread
    #process_thread.start()
    app.secret_key = 'some secret key'
    app.debug = True
    app.run(host=config.host, port=8080)
