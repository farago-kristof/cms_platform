import os

POSTGRES_CONNECTION = {
    'host': 'postgres',
    'port': 5432,
    'dbname': 'cms',
    'user': 'cms_user',
    'password': os.environ['POSTGRES_CMS_USER_PASSWORD'],
}

REDIS_CONNECTION = {
    'host': 'redis',
    'port': 6379
}

QUEUE_NAME = 'articles'
