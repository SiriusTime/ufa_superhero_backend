
DEBUG = False

#  DataBase
DB = {
    "name_db": "ufa",
    "user": "postgres",
    "password": "password",
    "host": "localhost",
    "client": "postgresql"
}

if not DEBUG:
    try:
        from local_settings import *
    except ImportError:
        pass

