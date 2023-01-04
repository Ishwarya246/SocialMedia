from flask import Flask, request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from models.models import db, User
import jwt, uuid, datetime

app = Flask(__name__)

app.config["SECRET_KEY"]='004f2af45d3a4e161a7dd2d17fdae47f'
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqldb://root:1234@localhost/SocialMedia"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

@app.route("/")
def home():
    return "Home Page"


def token_required(f):
   @wraps(f)
   def decorator(*args, **kwargs):
       token = None
       if "x-access-tokens" in request.headers:
           token = request.headers["x-access-tokens"]

       if not token:
           return jsonify({"status" : "Valid Token Missing"})
       try:
           data = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
           current_user = Users.query.filter_by(public_id = data["public_id"]).first()
       except:
           return jsonify({"status": "Invalid Token"})

       return f(current_user, *args, **kwargs)
   return decorator

@app.route("/signup", methods = ["POST", "GET"])
def signup():

    # if request.methods == 'GET':
    #     return "Hi"
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

        return jsonify({"status" : "Registered Successfully"})
    else:
        return jsonify({"status" : "User already exists"})

@app.route("/login", methods = ["POST", "GET"])
def login():

    # if request.method == 'GET':
    #     return "Hi"

    # data = request.form
    data = request.get_json()
    print(data)
    if not data or not data.get("email") or not data.get("password"):

        return jsonify({"status" : "Enter valid email or password"})

    user =  User.query.filter_by(email = data.get("email")).first()

    if not user:
        return jsonify({"status" : "No such Email ID"})

    if check_password_hash(user.password, data.get("password")):

        jwt_token = jwt.encode({"public_id" : user.public_id,
                                "exp" : datetime.datetime.utcnow() + datetime.timedelta(minutes = 10)},
                                app.config["SECRET_KEY"],
                                "HS256")
        return jsonify({"status" : "Success", "token" : jwt_token})

    else:
        return jsonify({"status" : "Wrong password"})

@app.route("/post")
@token_required
def post(current_user):
    data = request.get_json()
    if not data or not data["image"] or not data["msg"]:
        return jsonify({"status" : "Cannot post"})
