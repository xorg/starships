import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    FLASK_APP = os.environ["FLASK_APP"]
    try:
        SECRET_KEY = os.environ["SECRET"]
    except KeyError:
        SECRET_KEY = "dev-secret-key"


class Dev(Config):
    SQLALCHEMY_DATABASE_URI = f"sqlite:////{basedir}/dev_db.sqlite"
    DEBUG = True


class Test(Config):
    SQLALCHEMY_DATABASE_URI = f"sqlite:////{basedir}/test_db.sqlite"
    TESTING = True
    DEBUG = True
