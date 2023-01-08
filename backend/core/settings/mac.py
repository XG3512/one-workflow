import os


APP_ENV = 'dev'

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '64318ob@vbou7h50)b0a_pfda4d$bw2nhl4h*m$qo0_e_fxw=658!z*x'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# sqlite
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, '../core.db'),
#     }
# }

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    # },
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS':{'read_default_file': os.path.join(BASE_DIR, 'database.cnf'),}
        #数据库名
        # 'NAME' : 'csdn',
        # 'USER' : 'lmapp',
        # 'PASSWORD' : 'lmapp',
        # 'HOST' : '127.0.0.1',
        # 'PORT' : '8088',
    }
}
