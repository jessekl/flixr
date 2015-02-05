# INTRODUCTION

Fbone (Flask bone) is a [Flask](http://flask.pocoo.org) (Python microframework) template/bootstrap/boilerplate application, with best practices.

You can use it for

- learning Flask.
- kicking off your new project faster.


## FEATURES

### Frontend Framework

- [HTML5 Boilerplate](https://github.com/h5bp/html5-boilerplate).
- [jQuery](http://jquery.com/).
- [bootstrap](https://getbootstrap.com).

### Flask Extensions

- Handle **orm** with [SQLAlchemy](http://www.sqlalchemy.org).
- Handle **web forms** with [WTForms](http://wtforms.simplecodes.com/).
- Implement **user session management (signin/signout/rememberme)** with [Flask-Login](https://github.com/maxcountryman/flask-login).
- Implement **reset password via email** with [Flask-Mail](http://packages.python.org/Flask-Mail/).
- Implement **unit testing** with [Flask-Testing](http://packages.python.org/Flask-Testing/).
- Implement **external script (initdb/testing/etc)** with [Flask-Script](http://flask-script.readthedocs.org/en/latest/).
- Handle **i18n** with [Flask-Babel](http://packages.python.org/Flask-Babel/).

### Others

- Well designed structure for a **large project**.
- Quickly Deploy via [fabric](flask.pocoo.org/docs/patterns/fabric/).
- Admin interface.
- Homebaked logger.

## USAGE

Pre-required:

- git
- pip
- sqlite
- virtualenv

```
$ python manage.py runserver
```
Then open `http://127.0.0.1:5000`

**IMPORTANT**:

- Change `INSTANCE_FOLDER_PATH` in `fbone/utils.py` to suit yourself.
- Put `*.cfg` under `INSTANCE_FOLDER_PATH`.

```
## STRUCTURE

    ├── fbone                       (main app)
    │   ├── app.py                  (application factory)
    │   ├── config.py               (config module)
    │   ├── decorators.py           (route decorators)
    │   ├── extensions.py           (flask extensions)
    │   ├── modules                 (MVC modules)
    │   │   ├── admin               (admin module)
    │   │   ├── api                 (api module)
    │   │   ├── frontend            (frontend module)
    │   │   ├── settings            (settings module)
    │   │   └── user                (user module)
    │   │       ├── __init__.py
    │   │       ├── constants.py
    │   │       ├── forms.py
    │   │       ├── models.py
    │   │       └── views.py
    │   ├── static
    │   │   ├── css
    │   │   ├── img
    │   │   └── js
    │   ├── templates
    │   ├── translations            (i18n)
    │   ├── utils.py
    ├── LICENSE
    ├── manage.py                   (manage via flask-script)
    ├── README.md
    └── tests                       (unit tests, run via `nosetest`)
```

## LICENSE

[MIT LICENSE](http://www.tldrlegal.com/license/mit-license)

## ACKNOWLEDGEMENTS

Thanks to Python, Flask, its [extensions](http://flask.pocoo.org/extensions/), and other goodies.
