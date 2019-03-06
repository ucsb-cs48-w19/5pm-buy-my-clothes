import os
import string
import random
from base64 import b64encode
from datetime import datetime
from flask import Flask, render_template, request, url_for, redirect, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import validators

app = Flask(__name__)
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)

#DON'T TOUCH THIS LINE OF CODE WE NEED IT

#app.secret_key = ''.join(random.choices(string.ascii_letters, k=16))
app.secret_key = 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'

categoryNames = [
"womens-accessories",
"womens-bags",
"womens-coats",
"womens-dresses",
"womens-jeans",
"womens-jewelry",
"womens-pants",
"womens-rompers",
"womens-shirts-and-blouses",
"womens-shoes",
"womens-shorts",
"womens-skirts",
"womens-sweaters",
"womens-swimwear",
"womens-tshirts-and-tanks",
"mens-accessories",
"mens-coats",
"mens-pants",
"mens-shirts",
"mens-shoes",
"mens-shorts",
"mens-sweaters",
"mens-swim",
"mens-tshirts"]


###################################
#       TABLES IN OUR DATABASE    #
###################################

class imagePost(db.Model):
	id = db.Column(db.Integer, primary_key=True)

	image     = db.Column(db.LargeBinary)
	filename  = db.Column(db.Text, nullable=False)
	extension = db.Column(db.String(5), nullable=False)
	username  = db.Column(db.String(15), nullable=False)

	links     = db.Column(db.Text, nullable=False)
	category  = db.Column(db.Text, nullable=True)

	def __repr__(self):
		return '<Post %r, User %s, Filename %s, extension %s>' % (self.id, self.username, self.filename, self.extension)


class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)

	username = db.Column(db.String(15), nullable=False, unique=True)
	password = db.Column(db.String(300), nullable=False)
	email = db.Column(db.String(50), nullable=False, unique=True)

	def __repr__(self):
		return '<User %r>' % self.username


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

def pic_in_db(hash_val):
    """
    Args:
        hash_val(bytes obj): Hash value of uploaded pic

    Returns:
        Boolean true if pic in db, o.w. false

    """
    if imagePost.query.filter_by(hash_val=hash_val).count() > 0:
        return True
    return False


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
	return User.query.filter_by(username=username).count() == 1

def user_password(username):
	return User.query.filter_by(username=username).first().password

def user_email_exists(email):
	return User.query.filter_by(email=email).count() == 1

def check_legit_email(email):
	if "@" in email and "." in email and (email.find('@') < email.find('.')):
		return True
	else:
		return False

#Determines path to database
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(os.getcwd() , 'database/app.db')


#Disables useless warnings
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

@app.route('/')
def index():
    return clothes('all')

@app.route('/browse')
def browse():
    return render_template('browse.html')

@app.route('/browsemens')
def browsemens():
	return render_template('browsemens.html')

@app.route('/clothes/<category>')
def clothes(category):
	postList = get_all_items()

	#Makes list of all images
	imageList = []
	categoryList = []

	if category != 'all':
		for post in postList:
			categories = post.category.split()
			if category in categories:
				categoryList.append(post)

	else:
		categoryList = postList


	for post in categoryList:
		image = str(b64encode(post.image))[2:-1]

		#TODO: Make long string tuples with (descriptor, link) pair
		#TODO: Put into separate function
		category_link = ''
		for i in range(len(post.links.split())):
			category_link += post.category.split()[i] + ';' + post.links.split()[i] + ' '
		print(category_link)
		image_post_tuple = (post, image, category_link.strip())
		imageList.append(image_post_tuple)


	imageList = imageList[::-1]
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

@app.route('/upload', methods=['GET', 'POST'])
def upload():
	#Checks if the user is logged in to upload photos
	print(session)
	if 'username' in session:
		session.pop('urlInvalid', None)
		if request.method == 'POST':
			file = request.files['file']
			filename, extension = parse_filename(file.filename) #input sanitization

			#TODO: Make 404 or Error page template
			if filename == None or extension == None:
				return "oopsie woopsie you messed up"

			#TODO: Make this cleaner/less hackier

			count = len(request.form)
			index = 0
			categories = ''
			links = ''
			lastCategory = ''
			for key, value in request.form.items():
				index += 1
				if index > count - 1:
					if not value:
						break
					categories += lastCategory + ' '
				elif index > count - 2:
					lastCategory = value
					continue

				if 'selector' in key:
					categories += value + ' '
				elif 'link' in key:
					if not (validators.domain(value) or validators.url(value)):
						session['urlInvalid'] = True
						return render_template('upload.html', categoryNames=categoryNames)
					links += value + ' '

			categories = categories.strip()
			links = links.strip()

			new_file = imagePost(image=file.read(), filename=filename, extension=extension, username=session.get('username'), links=links, category=categories)

			db.session.add(new_file)
			db.session.commit()

			return redirect(url_for('index'))

		else:
			return render_template('upload.html', categoryNames=categoryNames)

	else:
		return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
	session.pop('noUser', None)
	session.pop('badPassword', None)

	if request.method == 'POST':

		username = request.form['username']
		password = request.form['password']

		if not user_in_db(username):
			session['noUser'] = True
			return render_template('login.html')

		if not bcrypt.check_password_hash(user_password(username),password):
			session['badPassword'] = True
			return render_template('login.html')

		else:
			session['username'] = username
			return redirect(url_for('index'))

	return render_template('login.html')

@app.route('/logout')
def logout():
	session.pop('username', None)
	return redirect(url_for('index'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
	session.pop('usernameExists', None)
	session.pop('emailExists', None)
	session.pop('invalidEmail', None)

	#form = RegistrationForm(request.form)
	if request.method == 'POST':

		username = request.form['username']
		email = request.form['email']
		password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')


		#Add user to database
		if not user_in_db(username) and not user_email_exists(email):

			#Check if email is legit
			if check_legit_email(email)==False:
				session['invalidEmail'] = True
				return render_template('signup.html')

			else:
				new_user = User(username=username, password=password, email=email)
				db.session.add(new_user)
				db.session.commit()



				session['username'] = username
				return redirect(url_for('index'))

		elif user_in_db(username):
			session['usernameExists'] = True
			return render_template('signup.html')
		elif user_email_exists(email):
			session['emailExists'] = True
			return render_template('signup.html')

	else:
		return render_template('signup.html')


if __name__ == "__main__":
	#Clears the DB on init so changes to db class don't create issues
	#NOTE: Since the flask app should only be ran once this won't continuously clear the db
	#db.drop_all()
	#db.create_all()

	#Runs the app
	app.run()
