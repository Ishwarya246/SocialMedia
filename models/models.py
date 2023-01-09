from flask_sqlalchemy import SQLAlchemy 

db = SQLAlchemy()

class User(db.Model) :

    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key = True)
    userid  = db.Column(db.String(100) , unique = True)
    name  = db.Column(db.String(100))
    email = db.Column(db.String(100))
    password = db.Column(db.String(256))
    photo = db.Column(db.Text(4294000000))
    validity = db.Column(db.Integer)


    def __init__(self, userid, name , email , password, photo ,  validity) :
        # self.id = id
        self.userid= userid
        self.name =  name
        self.email = email
        self.password = password 
        self.photo = photo
        self.validity = validity

    def as_dict(self) : 
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}


class Post(db.Model) :

    __tablename__ = "post"

    id = db.Column(db.Integer , primary_key = True)
    postid = db.Column(db.String(100), unique = True)
    userid = db.Column(db.String(100))  #foreign key
    image = db.Column(db.Text(4294000000))
    msg = db.Column(db.String(500))
    created_time = db.Column(db.DateTime)
    no_of_likes = db.Column(db.Integer)

    def __init__(self, postid, userid , image , msg , created_time , no_of_likes) :
        # self.id = id
        self.postid = postid
        self.userid = userid   # foreign key
        self.image = image
        self.msg = msg 
        self.created_time = created_time
        self.no_of_likes = no_of_likes

    def as_dict(self) : 
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}


class Comment(db.Model) :

    __tablename__ = "comment" 

    id = db.Column(db.Integer , primary_key =True)
    commentid = db.Column(db.String(100))
    userid = db.Column(db.String(100)) # foreign  key
    postid = db.Column(db.String(100)) #foreign key
    msg = db.Column(db.String(100))
    created_time = db.Column(db.DateTime)

    def __init__(self, commentid, userid , postid , msg , created_time) :
        # self.id = id
        self.commentid = commentid
        self.userid = userid
        self.postid = postid
        self.msg = msg 
        self.created_time = created_time

    def as_dict(self) :
        return {c.name: str(getattr(self , c.name)) for c in self.__table__.columns}


class Like(db.Model):

    __tablename__ = "likes" 

    id = db.Column(db.Integer , primary_key = True)
    userid = db.Column(db.String(100)) #foreign key
    postid = db.Column(db.String(100))

    def __init__(self, userid, postid):
        # self.id = id
        self.userid = userid
        self.postid = postid

    def as_dict(self) :
        return {c.name: str(getattr(self , c.name)) for c in self.__table__.columns}
