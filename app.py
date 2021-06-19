import os
import urllib.request
from flask import Flask, flash, request, redirect, url_for, render_template, send_file
from werkzeug.utils import secure_filename
from PIL import Image
import cnnmodel
from cnnmodel import prediction_result


UPLOAD_FOLDER = 'static/uploads/images'
app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

prediction_disease = ""


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def upload_form():
    return render_template('upload1.html')


@app.route('/', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading', "danger")
        return redirect(url_for('upload_form'))
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        img = Image.open(r"static/uploads/images/"+str(filename))
        img = img.resize([224, 224])
        img.save("test/test/"+str(filename))
        prediction_of_disease = prediction_result()[0]
        if os.path.exists("test/test/"+str(filename)):
            os.remove("test/test/"+str(filename))
        global prediction_disease
        prediction_disease = prediction_of_disease
        return render_template('upload1.html', filename=filename, disease=prediction_of_disease)
    else:
        flash('Allowed image types are -> png, jpg, jpeg')
        return redirect(request.url)


@app.route('/display/<filename>')
def display_image(filename):
    return redirect(url_for('static/uploads/images', filename=filename), code=301)


@app.route('/download-result')
def download_result():
    global prediction_disease
    f = open("results.txt", 'w')
    f.write("Disease name : {}".format(prediction_disease))
    f.close()
    prediction_disease = ""
    return send_file("results.txt", as_attachment=True)


if __name__ == "__main__":
    app.run()
