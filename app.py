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
		return None, None

	filename = lst[0].lower()
	extension = lst[-1].lower()

	if(extension not in ACCEPTED_EXTENSIONS):
		return None, None

	return filename, extension


#Determines path to database
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(os.getcwd() , 'database/app.db')

#Disables useless warnings
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

	#Makes list of all images
	imageList = []
	for post in postList:
		image = str(b64encode(post.image))[2:-1]

		#TODO: Make long string tuples with (descriptor, link) pair
		#TODO: Put into separate function
		category_link = ''
		for i in range(len(post.body.split())):
			category_link += post.category.split()[i] + ';' + post.body.split()[i] + ' '
			print(category_link)
		image_post_tuple = (post, image, category_link.strip())
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

	return render_template('clothes.html', pic_col1=col1[::-1], pic_col2=col2[::-1], pic_col3=col3[::-1])

@app.route('/upload', methods=['GET', 'POST'])
def upload():
	if request.method == 'POST':
		file = request.files['file']
		filename, extension = parse_filename(file.filename) #input sanitization

		#TODO: Make 404 or Error page template
		if filename == None or extension == None:
			return "oopsie woopsie you messed up"

		#TODO: Make this cleaner/less hackier
		count = 0
		key = 'category-link-'
		links = ''
		while request.form.get(key + str(count)):
			link = request.form.get(key + str(count))
			print(link)
			links += link + ' '
			count += 1

		body = links.strip()
		category = request.form['category'].strip()
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
