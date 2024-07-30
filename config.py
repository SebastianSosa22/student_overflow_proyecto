import os


class Config:
    SECRET_KEY = os.environ.get(
        'SECRET_KEY') or '9586e0373c6d447892502adb79715a48'
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL') or 'postgresql://admin:miadmin123@127.0.0.1:5432/studentoverflow'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt_secret_key'
