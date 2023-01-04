from flask import Flask
from werkzeug.security import generate_password_hash, check_password_hash
from models import models
import jwt, uuid

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://root:1234@localhost/SocialMedia'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
models.db.init_app(app)

@app.route("/")
def home():
    return "Home Page"
