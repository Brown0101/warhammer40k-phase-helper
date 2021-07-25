import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_USER = os.environ.get("DATABASE_USER")
DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD")
DATABASE_HOST = os.environ.get("DATABASE_HOST")
DATABASE_NAME = os.environ.get("DATABASE_NAME")
FLASK_APP = os.environ.get("FLASK_APP")
FLASK_ENV = os.environ.get("FLASK_ENV")
FLASK_DEBUG = os.environ.get("FLASK_DEBUG")
SECRET_KEY = os.environ.get("SECRET_KEY")
SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}/{DATABASE_NAME}"
SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get("SQLALCHEMY_TRACK_MODIFICATIONS")
