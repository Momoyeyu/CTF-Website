"""
Django settings for backend project.

Generated by 'django-admin startproject' using Django 4.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-^wh902yfpgf+p3f_rage%h%#d741nqfanx*-9xe(60a+x)m*vr'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    'localhost',
    '8.130.98.1',
]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 跨域资源共享（便于前后端联调）
    'corsheaders',

    # 自设计库表
    'tasks.apps.TasksConfig',
    'rank.apps.RankConfig',
    'common.apps.CommonConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # CORS跨域资源共享
    'corsheaders.middleware.CorsMiddleware',

    # csrf 中间件，此处设置会在全局生效
    # 'django.middleware.csrf.CsrfViewMiddleware',
]

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'backend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
# DATABASES = {
#   'default': {
#       'ENGINE': 'django.db.backends.mysql',
#       'NAME': 'ezctf_top',   # 数据库名
#       'USER': 'ezctf_top',    # 数据库 用户名
#       'PASSWORD': 'yfr4FaRtPr6eZEYz',# 数据库 用户密码
#       'HOST': '127.0.0.1', # 数据库服务主机名
#       'PORT': '3306',      # 数据库服务端口
#       'CONN_MAX_AGE': 0
#   }
# }

"""Gunicorn"""
GUNICORN_CONFIG = {
    'bind': '0.0.0.0:8000',
    'workers': 4,
    'timeout': 60,
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',  # 使用ModelBackend进行用户身份验证
    # 其他自定义身份验证后端，如果需要的话
]

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# CORS跨域资源共享
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

# CORS_ALLOWED_ORIGINS = [
#     "http://localhost:8080",
#     "http://localhost:8000",
#     "http://localhost:80",
#     "ezctf.top",
#     # 允许其他需要的域名
# ]


# session
SESSION_ENGINE = 'django.contrib.sessions.backends.db'

# 邮箱设置
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.qq.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = '3296989473@qq.com'
EMAIL_HOST_PASSWORD = 'sdxuhyrrvzvkcide'
# EMAIL_USE_SSL = True


# 媒体文件
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

ONLINESCENE_ROOT = os.path.join(BASE_DIR,'probs')

LOGIN_URL = 'http://localhost:8080/#/Login'

# CSRF
# CSRF_COOKIE_HTTPONLY = False
# CSRF_COOKIE_AGE = 31449600
# CSRF_COOKIE_NAME = 'csrftoken'
# CSRF_USE_SESSIONS = False
# CSRF_FAILURE_VIEW = 'django.views.csrf.csrf_failure'
#
# X_FRAME_OPTIONS = "SAMEORIGIN"


