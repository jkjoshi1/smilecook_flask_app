class Config:

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://python_api:joshi@localhost/smilecook_tryagain'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'super_secret_key'
    JWT_ERROR_MSG_KEY ='message'