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
	filename = db.Column(db.Text, nullable=False)
	extension = db.Column(db.String(5), nullable=False)
	#hash_val = db.Column(db.String(32), nullable=True)
	#body = db.Column(db.Text, nullable=False)
	#category = db.Column(db.Text, nullable=True)
	#pub_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	def __repr__(self):
		return '<Post %r>' % self.id

def get_item(_id):
    obj = imagePost.query.filter_by(id=_id).first()
    return obj

def get_filename(name):
    return imagePost.query.filter_by(filename=name).first()

def parse_filename(in_string):

	ACCEPTED_EXTENSIONS = {'png', 'jpeg', 'gif'}
	lst = in_string.split('.')

	if (len(lst) != 2):
		return None

	filename = lst[0]
	extension = lst[-1]

	if(extension not in ACCEPTED_EXTENSIONS):
		return None

	return filename, extension

	
 
#Uncomment for deployment
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')

#Comment for local testing
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.getcwd() , 'database/app.db')
print(app.config['SQLALCHEMY_DATABASE_URI'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/test')
def test_route():
	imagePost = get_item(1)
	image = str(b64encode(imagePost.image))[2:-1] #string parsing for python
	return render_template('test.html', imagePost=imagePost, image=image)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
	if request.method == 'POST':
		file = request.files['file']
		filename, extension = parse_filename(file.filename) #input sanitization
		
		if filename == None or extension == None:
			return "oopsie woopsie you messed up"

		new_file = imagePost(image=file.read(), filename=filename, extension=extension)

		db.session.add(new_file)
		db.session.commit()

		return file.filename + "uploaded!"

	else:
		return render_template('upload.html')

if __name__ == "__main__":
	app.run()
