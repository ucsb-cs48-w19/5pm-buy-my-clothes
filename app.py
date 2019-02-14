import os
from base64 import b64encode
from datetime import datetime
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)

class imagePost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.LargeBinary)
    filename = db.Column(db.Text, nullable=True)
    #hash_val = db.Column(db.String(32), nullable=True)
    #body = db.Column(db.Text, nullable=False)
    #category = db.Column(db.Text, nullable=True)
    #pub_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return '<Post %r>' % self.id


def get_item(_id):
    obj = imagePost.query.filter_by(id=_id).first()
    if obj == None:
        print("NONETYPE AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
        return None
    return obj

def get_filename(name):
    return imagePost.query.filter_by(filename=name).first()

#Uncomment for deployment
#app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')

#Comment for local testing
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.getcwd() , 'database/app.db')
print(app.config['SQLALCHEMY_DATABASE_URI'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/test')
def test_route():
    posts = get_filename('KEM.png')
    #print (posts.hash_val)
    image = str(b64encode(posts.image))[2:-1]
    print(image)
    return render_template('test.html', imagePost=posts, image=image)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':

        file = request.files['file'] 
        filename = file.filename

        new_file = imagePost(image=file.read(), filename=filename)

        db.session.add(new_file)
        db.session.commit()

        return file.filename

    else:
        return render_template('upload.html')

if __name__ == "__main__":
    app.run()

