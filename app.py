from flask import Flask, request, make_response, render_template
from werkzeug.security import generate_password_hash, check_password_hash
from models.database import db, User
import jwt, uuid

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://root:1234@localhost/SocialMedia'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route("/")
def home():
    return render_template('Test.html')

@app.route("/signup")
def signup():
    data = request.form

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email = email).first()

    if not user:
        user = User(public_id = str(uuid.uuid4()),
                    name = name,
                    email = email,
                    password = generate_password_hash(password))

        db.session.add(user)
        db.session.commit()

        return make_response('Registered Successfully')
    else:
        return make_response('User already exists')
