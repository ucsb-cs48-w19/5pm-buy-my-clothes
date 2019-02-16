import os
import hashlib
from base64 import b64encode
from datetime import datetime
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)

class imagePost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image     = db.Column(db.LargeBinary, nullable=False)
    filename  = db.Column(db.Text, nullable=False)
    extension = db.Column(db.String(5), nullable=False)
    hash_val  = db.Column(db.LargeBinary, nullable=False)
    body      = db.Column(db.Text, nullable=False)
    category  = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return '<Post %r>' % self.id

def get_item(_id):
    obj = imagePost.query.filter_by(id=_id).first()
    return obj

def get_all_items():
    objs = imagePost.query.all()
    return objs

def get_filename(name):
    return imagePost.query.filter_by(filename=name).first()

def pic_in_db(hash_val):
    """
    Args:
        hash_val(bytes obj): Hash value of uploaded pic

    Returns: 
        Boolean true if pic in db, o.w. false

    """
    if imagePost.query.filter_by(hash_val=hash_val).count() > 1:
        return True
    return False


def parse_filename(in_string):

    ACCEPTED_EXTENSIONS = {'png','jpg', 'jpeg', 'gif'}
    lst = in_string.split('.')

    if (len(lst) != 2):
            return None, None

    filename = lst[0]
    extension = lst[-1]

    if(extension not in ACCEPTED_EXTENSIONS):
            return None, None

    return filename, extension

def hash_image(image):
    """
    Args:
        image(Bytes obj): Pass image as bytes obj

    Returns: 
        (Bytes obj): 256 Hash of the input picture

    """
    m = hashlib.sha256()
    m.update(image)
    
    return m.digest()


#Uncomment for deployment
#app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')

#Uncomment for local testing
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.getcwd() , 'database/app.db')


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

@app.route('/')
def index():
    return redirect(url_for('clothes'))

@app.route('/browse')
def browse():
    return render_template('browse.html')

@app.route('/clothes')
def clothes():
    postList = get_all_items()

    imageList = []
    for post in postList:
        image = str(b64encode(post.image))[2:-1]
        image_post_tuple = (post, image)
        imageList.append(image_post_tuple)

    col1 = []
    col2 = []
    col3 = []

    for i in range(len(imageList)):
        if i % 3 == 0:
            col1.append(imageList[i])
        elif i % 3 == 1:
            col2.append(imageList[i])
        elif i % 3 == 2:
            col3.append(imageList[i])

    col1 = col1[::-1]
    col2 = col2[::-1]
    col3 = col3[::-1]

    return render_template('clothes.html', pic_col1=col1, pic_col2=col2, pic_col3=col3)

@app.route('/test')
def test_route():
    imagePosts = get_all_items()
    for i in range(len(imagePosts)):
        imagePosts[i].image = str(b64encode(imagePosts[i].image))[2:-1] #string parsing for python

    return render_template('test.html', imagePosts=imagePosts)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']

        filename, extension = parse_filename(file.filename) #input sanitization

        if filename == None or extension == None:
            return "OOPSIE WOOPSIE WE MADE A FUCKO BOINGO"

        hash_val = hash_image(file.read()) 

        body = request.form['description']
        category = request.form['category']
        print('body', body)
        print('category', category)

        #TODO: Make an actual "error/404 page"
        #if pic_in_db(hash_val):
        #    return url_for('clothes')
        
        new_file = imagePost(image=file.read(), filename=filename, hash_val=hash_val, extension=extension, body=body, category=category)

        db.session.add(new_file)
        db.session.commit()

        return redirect(url_for('clothes'))

    else:
        return render_template('upload.html')

if __name__ == "__main__":
	app.run()
