##DB URL (DATABASE_URL)
<postgres://haezqswxdtwsyg:4f67fdd699eec15173563272e5763977049af5d9bc308e1fc28accfccb91924c@ec2-54-247-166-129.eu-west-1.compute.amazonaws.com:5432/d4mqogcp0i0r3s>

##Google OAuth
client ID
```
445215232007-odl1jus5p01sn4a4og8j8f6ssb9p886c.apps.googleusercontent.com
```
client secret
```
Rzxr9_kQPu1lPJupkDHAk1aw
```

# Based on python-getting-started

A barebones Python app, which can easily be deployed to Heroku.

This application supports the [Getting Started with Python on Heroku](https://devcenter.heroku.com/articles/getting-started-with-python) article - check it out.

## Running Locally

Make sure you have Python [installed properly](http://install.python-guide.org).  Also, install the [Heroku Toolbelt](https://toolbelt.heroku.com/) and [Postgres](https://devcenter.heroku.com/articles/heroku-postgresql#local-setup).

```sh
$ git clone git@github.com:heroku/python-getting-started.git
$ cd python-getting-started

$ pip install -r requirements.txt

$ createdb python_getting_started

$ python manage.py migrate
$ python manage.py collectstatic

$ heroku local
```

Your app should now be running on [localhost:5000](http://localhost:5000/).

## Deploying to Heroku

```sh
$ heroku create
$ git push heroku master

$ heroku run python manage.py migrate
$ heroku open
```
or

[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy)

## Documentation

For more information about using Python on Heroku, see these Dev Center articles:

- [Python on Heroku](https://devcenter.heroku.com/categories/python)
