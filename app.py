from flask import Flask, render_template, \
                  request, url_for, flash
from werkzeug.utils import secure_filename
import os

PATH_TO_PICTURE = os.getcwd() + '/static/images/'
ALLOWED_EXTENSIONS = ['gif', 'png', 'jpg', 'tiff']
SECRET_KEY = 'AAAAAAAAAAAAAAA'

app = Flask(__name__)
app.config['UPLOAD_PHOTO'] = PATH_TO_PICTURE
app.secret_key = SECRET_KEY

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        print("FILE PATH IS : ", app.config['UPLOAD_PHOTO'])
        #check if the post request has the file
        if 'file' not in request.files:
            return redirect(request.url)

        _file = request.files['file']

        if _file and allowed_file(_file.filename):
            filename = secure_filename(_file.filename)
            _file.save(os.path.join(app.config['UPLOAD_PHOTO'], filename))
            flash('Upload Complete!')
            return render_template('index.html')

    else: #This is the case for the get request 
        return render_template('upload.html')

 
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run()
