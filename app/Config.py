class Config(object):
    DEBUG = True
    TESTING = True
    SECRET_KEY = "abcdefghijklmnopqrstuvwxyz1234567890%$%&**%$"
    USER = 'imdb'
    PWD = '^YHNnhy6'
    DBNAME = 'imdb'
    HOST = 'localhost'
    PORT = '3306'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'mysql://imdb:^YHNnhy6@localhost:3306/imb'
    #SQLALCHEMY_DATABASE_URI = 'mysql://{}:{}@{}:{}/{}'.format(USER, PWD, HOST, PORT, DBNAME)


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