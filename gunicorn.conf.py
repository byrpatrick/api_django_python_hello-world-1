from os import environ
from dotenv import load_dotenv

load_dotenv()
SERVER_PORT = environ.get("PORT") or 6060

wsgi_app = "hello_world.wsgi"
bind = f"0.0.0.0:{SERVER_PORT}"
