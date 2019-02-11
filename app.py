from flask import Flask, render_template, flash, \
                  request, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':

        #check if the post request has the file
        if 'file' not in request.files:
            flash('no file part')
            return redirect(request.url)

        _file = request.files['file']

        if _file.filename == '':
            flash('No file selected')

        if _file and allowed_file(_file.filename):
            filename = secure_filename(_file.filename)
            _file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('upload_file', filename=filename))

 
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run()
