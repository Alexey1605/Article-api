import os

SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URL', 'postgres')
