from dotenv import load_dotenv
from os import getenv, environ


load_dotenv()

TOKEN = getenv('TOKEN')
IS_DEBUG = environ.get('IS_DEBUG', 'false').lower() == 'true'