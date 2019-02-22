import os
import string
import random
from base64 import b64encode
from datetime import datetime
from flask import Flask, render_template, request, url_for, redirect, session, flash
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import bcrypt

app = Flask(__name__)
db = SQLAlchemy(app)

#DON'T TOUCH THIS LINE OF CODE WE NEED IT
app.secret_key = ''.join(random.choices(string.ascii_letters, k=16))


###################################
#       TABLES IN OUR DATABASE    #
###################################

class imagePost(db.Model):
	id = db.Column(db.Integer, primary_key=True)

	image     = db.Column(db.LargeBinary)
	filename  = db.Column(db.Text, nullable=False)
	extension = db.Column(db.String(5), nullable=False)
	
	body      = db.Column(db.Text, nullable=False)
	category  = db.Column(db.Text, nullable=True)

	def __repr__(self):
		return '<Post %r, Filename %s, extension %s>' % self.id, self.filename, self.extension


class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)

	username = db.Column(db.String(15), nullable=False, unique=True)
	password = db.Column(db.String(300), nullable=False)


###################################
#  HELPER FUNCTIONS FOR DB ACCESS #
###################################

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

def user_in_db(username):
	return User.query.count() == 1

def user_password(username):
	return User.query.filter_by(username=username).first().password



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

@app.route('/login', methods=['GET', 'POST'])
def login(): 
	if request.method == 'POST':

		username = request.form['username']
		password = bcrypt.encrypt(request.form['password'])

		if not user_in_db(username):
			return "Error: User not found"

		if password != user_password(username):
			return "Error: Wrong password"

		else: 
			session['username'] = 'username'
			return redirect(url_for('uploads.html'))

	return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
	#form = RegistrationForm(request.form)
	if request.method == 'POST':

		username = request.form['username']
		password = bcrypt.encrypt(request.form['password'])

		#Add user to database
		if not user_in_db(username):

			new_user = User(username=username, password=password)
			db.session.add(new_user)
			db.session.commit()

			return 'Account created for user : ' + username + '<br>With password : ' + password

		else: 
			return 'You\'re already in here silly!'

	else:
		return render_template('register.html')


if __name__ == "__main__":
	#Clears the DB on init so changes to db class don't create issues
	#NOTE: Since the flask app should only be ran once this won't continuously clear the db
	db.drop_all()
	db.create_all()

	#Runs the app
	app.run()
