from flask import Flask
from .main import configure_routes

app = Flask(__name__)
configure_routes(app)
