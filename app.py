from flask import Flask
from werkzeug.security import generate_password_hash, check_password_hash
import models, jwt, uuid

app = Flask(__name__)

#db.init_app(app)

@app.route("/")
def home():
    return "Home Page"
