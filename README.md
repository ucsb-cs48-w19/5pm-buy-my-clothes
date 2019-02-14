# Shop My Style

## Project summary
A web app for you to show off your style to others and browse new outfits to shop.

### Additional information about the project

You can upload pictures of your outfit anytime, anywhere for others to view. You can browse photos from other users, find the brands you know you love or find all new styles to wear.

https://shop-my-style.herokuapp.com/

## Installation

### Prerequisites

- Python3
- pip
- flask
- flask_sqlalchemy
- alembic
- flask_script
- flask_migrate
- psycopg2
- gunicorn


### Installation Steps

Download the latest version of [Python3](https://www.python.org/downloads/) and [pip](https://pypi.org/project/pip/).

Run the following commands
```
pip3 install flask flask_sqlalchemy alembic flask_script flask_migrate psycopg2 gunicorn --user
```

Clone our directory
`git clone git@github.com:ucsb-cs48-w19/5pm-buy-my-clothes.git`

Next, cd into your project directory 
`cd 5pm-buy-my-clothes`

## Run application locally

Open a python shell 
`python3` 

Create a local database
```
from app import db
db.create_all()
```
Run app 
`FLASK_APP=app.py flask run`

`should be running on http://localhost:5000/ `

## Run application on heroku

Login to Heroku 
`heroku login` 

Create a new Heroku app 
`heroku create APP_NAME_HERE`

Lanch Heroku app:
`git push heroku master`

Now let us Set up the database on Heroku:

Create a Postgresql database by running the command 
`heroku addons:add heroku-postgresql:hobby-dev`

Now we need to initialze a table by running the following commands:
`heroku run python3`
  `from app import db`
  `db.create_all()`
  `exit()`

## Functionality

From the home page, browse clothes by category, or search if you know what you're looking for. Click on the images for descriptions of the outfits and links to where to buy them. To upload images, click on upload. Choose your photo and write a quick description. Copy and paste the links to where to buy your outfit in the description box.

## Known Problems

The web app doesn’t work...

## Contributing

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request :D

## License

If you haven't already, add a file called `LICENSE.txt` with the text of the appropriate license.
We recommend using the MIT license: <https://choosealicense.com/licenses/mit/>
