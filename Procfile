web: gunicorn -w 4 -b "0.0.0.0:$PORT" app:app
init: python3 manage.py db init
migrate: python3 manage.py db migrate
upgrade: python3 manage.py db upgrade
