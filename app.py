import os
import string
import random
from base64 import b64encode
from datetime import datetime
from flask import Flask, render_template, request, url_for, redirect, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)

#DON'T TOUCH THIS LINE OF CODE WE NEED IT

#app.secret_key = ''.join(random.choices(string.ascii_letters, k=16))
app.secret_key = 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'


###################################
#       TABLES IN OUR DATABASE    #
###################################

class imagePost(db.Model):
	id = db.Column(db.Integer, primary_key=True)

	image     = db.Column(db.LargeBinary)
	filename  = db.Column(db.Text, nullable=False)
	extension = db.Column(db.String(5), nullable=False)

	links     = db.Column(db.Text, nullable=False)
	category  = db.Column(db.Text, nullable=True)

	def __repr__(self):
		return '<Post %r, Filename %s, extension %s>' % self.id, self.filename, self.extension


class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)

	username = db.Column(db.String(15), nullable=False, unique=True)
	password = db.Column(db.String(300), nullable=False)
	email = db.Column(db.String(50), nullable=False, unique=True)


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
    if imagePost.query.filter_by(hash_val=hash_val).count() > 1:
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
			if category in post.category:
				categoryList.append(post)

	else:
		categoryList = postList


	for post in categoryList:
		image = str(b64encode(post.image))[2:-1]

		#TODO: Make long string tuples with (descriptor, link) pair
		#TODO: Put into separate function
		category_link = ''
		for i in range(len(post.links
		.split())):
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
				links += link + ' '
				count += 1


			links = links.strip()
			category = request.form['category'].strip()

			new_file = imagePost(image=file.read(), filename=filename, extension=extension, links=links, category=category)

			db.session.add(new_file)
			db.session.commit()

			return redirect(url_for('index'))

		else:
			return render_template('upload.html')

	else:
		return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':

		username = request.form['username']
		password = request.form['password']

		if not user_in_db(username):
			return "Error: User not found"

		if not bcrypt.check_password_hash(user_password(username),password):
			return "Password given : " + password + '<br>Password Expected : ' + user_password(username)

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
	#form = RegistrationForm(request.form)
	if request.method == 'POST':

		username = request.form['username']
		email = request.form['email']
		password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')


		#Add user to database
		if not user_in_db(username) and not user_email_exists(email):

			#Check if email is legit
			if check_legit_email(email)==False:
				return 'Invalid email'

			else:
				new_user = User(username=username, password=password, email=email)
				db.session.add(new_user)
				db.session.commit()



				session['username'] = username
				return redirect(url_for('index'))
				#return 'Account created for user : ' + username + '<br>With password : ' + password

		elif user_in_db(username):
			return 'You\'re already in here silly!'
		elif user_email_exists(email):
			return 'Account with this email address already exists'

	else:
		return render_template('signup.html')


if __name__ == "__main__":
	#Clears the DB on init so changes to db class don't create issues
	#NOTE: Since the flask app should only be ran once this won't continuously clear the db
	#db.drop_all()
	#db.create_all()

	#Runs the app
	app.run()
