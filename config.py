import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
class Config(object):
    DEBUG = True
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'red-hot-chilli-pepper'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    #UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads/')
    UPLOAD_FOLDER = '.'
    MAX_CONTENT_PATH = 1024*1024

class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True