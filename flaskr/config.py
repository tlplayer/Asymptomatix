import os

class Config(object):
    # WTform stuff. I think it's security-related.
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'this-is-the-key'

    # Database stuff. We're Using SQLite for now.
    SQLALCHEMY_DATABASE_URI = 'sqlite:///cases.db'
    # This just tells SQlALCHEMY the app doesn't need to know when a change is
    # being made to the database.
    SQLALCHEMY_TRACK_MODIFICATIONS = False