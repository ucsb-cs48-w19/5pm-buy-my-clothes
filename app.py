from datetime import datetime
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
#from models import db, Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/test')
def test_route():
    #posts = get_posts()
    return render_template('test.html')

if __name__ == "__main__":
    app.run()

def get_posts():
    return Post.query.all()

def get_post(id):
    return Post.query.filter_by(id=id).first()

def add_post(image, body, category):
    post = Post(image=image, body=body, category=category)
    db.session.add(post)
    db.session.commit()

'''
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username
'''

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(120), unique=True, nullable=False)
    body = db.Column(db.Text, nullable=False)
    category = db.Column(db.Text, nullable=True)
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return '<Post %r>' % self.id
