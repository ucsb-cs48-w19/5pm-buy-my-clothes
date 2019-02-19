import os
from base64 import b64encode
from datetime import datetime
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)

class imagePost(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	image = db.Column(db.LargeBinary)
	filename = db.Column(db.Text, nullable=False)
	extension = db.Column(db.String(5), nullable=False)
	#hash_val = db.Column(db.String(32), nullable=True)
	body = db.Column(db.Text, nullable=False)
	category = db.Column(db.Text, nullable=True)
	pub_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
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

def parse_filename(in_string):

	ACCEPTED_EXTENSIONS = {'png','jpg', 'jpeg', 'gif'}
	lst = in_string.split('.')

	if (len(lst) != 2):
		return None

	filename = lst[0].lower()
	extension = lst[-1].lower()

	if(extension not in ACCEPTED_EXTENSIONS):
		return None

	return filename, extension


#Uncomment for deployment
#app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')

#Comment for local testing
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.getcwd() , 'database/app.db')
print(app.config['SQLALCHEMY_DATABASE_URI'])
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
			return "oopsie woopsie you messed up"
		#body = 'This is the body'
		#category = 'category'
		body = request.form['description']
		category = request.form['category']
		print('body', body)
		print('category', category)
		new_file = imagePost(image=file.read(), filename=filename, extension=extension, body=body, category=category)

		db.session.add(new_file)
		db.session.commit()

		return redirect(url_for('clothes'))

	else:
		return render_template('upload.html')

if __name__ == "__main__":
	app.run()
