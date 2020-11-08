import os
from dotenv import load_dotenv
load_dotenv()


config = {
    'connections': {
        'default': {
            'engine': 'tortoise.backends.asyncpg',
            'credentials': {
                'host': os.getenv('DB_HOST'),
                'port':os.getenv('DB_PORT'),
                'user': os.getenv('DB_USER'),
                'password': os.getenv('DB_PASSWORD'),
                'database': os.getenv('DB_DATABASE'),
                'maxsize':'30'
            }
        },
    },
    'apps': {
        'models': {
            'models': [""],
            'default_connection': 'default',
        }
    }
}

