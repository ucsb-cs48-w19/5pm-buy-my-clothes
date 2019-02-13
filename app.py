import os
from datetime import datetime
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)

def get_posts():
    return Post.query.all()

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.LargeBinary)
    body = db.Column(db.Text, nullable=False)
    category = db.Column(db.Text, nullable=True)
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return '<Post %r>' % self.id

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
    posts = get_posts()
    
    return render_template('test.html', posts=posts)

if __name__ == "__main__":
    app.run()

