# Run
python code/app.py
## INSTALL FLASK
pip install flask

## Create virtual enviroment
> GO IN
```
pip install virtualenv
virtualenv venv --python=python3.8.3
# NOT ON WINDOWS = source venv/bin/activate or source venv/scripts/activate
# ON WINDOWS = ./venv/Scripts/activate.bat
```
> EXIT
```bash
deactivate
```
### Instal FlaskResfull
```
pip install Flask-RESTful
```

### AUTH FLASK JWT INSTALL
```
pip install Flask-JWT
```

### SQL Database
> Create tables
```
python code/create_tables.py
```

### flask_sqlalchemy
```
pip install flask_sqlalchemy
```
or 
```
pip install -U Flask-SQLAlchemy
```

### HEROKU DEPLOY
1. create runtime.txt and add python version.  (example: python-3.8.3)
2. create requirements.txt
```txt
Flask
FlaskRESTful
Flask-JWT
Flask-SQLAlchemy
uwsgi
```
3. create uwsgi.ini file
```ini
[uwsgi]
http-socket = :$(PORT)
master = true
die-on-term=true
module = app:app
memory-report = true
```
4. create ProcFile
```ProcFile
web: uwsgi uwsgi.ini
```