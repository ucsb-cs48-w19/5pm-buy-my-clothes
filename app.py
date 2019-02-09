from flask import Flask, render_template, flash, \
                  request, url_for

app = Flask(__name__)

ALLOWED_EXTENSIONS = {'jpg', 'png', 'gif'}

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


    file = request.files['file']

    if file.filename == '':
        flash('

 
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run()
