
### HEROKU DEPLOY
1. Add runtime.txt to root of project.
```txt
python-3.8.3
```
2. create requirements.txt
```txt
Flask
FlaskRESTful
Flask-JWT
Flask-SQLAlchemy
uwsgi
psycopg2
```
3. create uwsgi.ini file
```ini
[uwsgi]
http-socket = :$(PORT)
master = true
die-on-term=true
module = run:app
memory-report = true
```
4. create ProcFile
```ProcFile
web: uwsgi uwsgi.ini
```

5. Create project in Heroku from GIT and under settings add Buildpack. `heroku/python`

6. Run Manual Deploy from GIT in Heroku project.


## Add HEROKU_POSTGRES
1. Go to Addons and add Heroku Postgres
2. Once you install it you will have a config variable named DATABASE_URL in heroku.