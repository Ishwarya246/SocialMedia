from flask import Flask, request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from flask_cors import CORS
from models.models import db, User, Like, Post
import jwt, uuid, datetime

app = Flask(__name__)
CORS(app)

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
       if "Authorization" in request.headers:
           token = request.headers["Authorization"]

       if not token:
           return jsonify({"status" : "Valid Token Missing"})

       token = str.replace(str(token), 'Bearer ', '')

       try:
           data = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
           # , options={'verify_exp': False}
           current_user = User.query.filter_by(userid = data["userid"]).first()

       except:
           return jsonify({"status": "Invalid Token"})

       return f(current_user, *args, **kwargs)
   return decorator

@app.route("/signup", methods = ["POST"])
def signup():

    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email = email).first()

    if not user:
        user = User(userid = str(uuid.uuid4()),
                    name = name,
                    email = email,
                    password = generate_password_hash(password))

        db.session.add(user)
        db.session.commit()

        return jsonify({"status" : "Success"})
    else:
        return jsonify({"status" : "User already exists"})

@app.route("/login", methods = ["POST"])
def login():
    data = request.get_json()
    print(data)
    if not data or not data.get("email") or not data.get("password"):

        return jsonify({"status" : "Enter valid email or password"})

    user =  User.query.filter_by(email = data.get("email")).first()

    if not user:
        return jsonify({"status" : "No such Email ID"})

    if check_password_hash(user.password, data.get("password")):

        jwt_token = jwt.encode({"userid" : user.userid, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(days=365, seconds=0)},
                                app.config["SECRET_KEY"])
        return jsonify({"status" : "Success", "token" : jwt_token})

    else:
        return jsonify({"status" : "Wrong password"})

@app.route("/post", methods = ["POST"])
@token_required
def post(current_user):
    data = request.get_json()

    if not data or not data["image"] or not data["msg"]:
        return jsonify({"status" : "Cannot post"})

    record = Post(str(uuid.uuid4()), current_user.userid , data["image"] ,data["msg"] ,datetime.datetime.utcnow(), 0)

    db.session.add(record)
    db.session.commit()

    return jsonify({"status" : "Posted Successfully"})

@app.route("/like", methods = ["POST"])
@token_required
def like(current_user):
    data = request.get_json()

    if not data or not data["postid"]:
        return jsonify({"status" : "Invalid Post ID"})

    post = Post.query.filter_by(postid = data["postid"]).first()

    like = Like.query.filter_by(userid = current_user.userid).filter_by(postid = data["postid"]).first()

    if not like:
        record = Like(current_user.userid, data["postid"])
        db.session.add(record)
        setattr(post, "no_of_likes", post.no_of_likes + 1)

    else:
        Like.query.filter_by(userid = current_user.userid).delete()
        setattr(post, "no_of_likes", post.no_of_likes - 1)

    db.session.commit()
    return jsonify({"status" : "Success"})


