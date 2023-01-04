from flask_sqlalchemy import SQLAlchemy 

db = SQLAlchemy()

class User(db.Model) :

    __tablename__ = "user"
    id = db.Column(db.Integer , primary_key = True)
    public_id  = db.Column(db.String(100) , unique = True)
    name  = db.Column(db.String(100))
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))


    def __init__(self, id , public_id, name , email , password) :
        self.id = id 
        self.public_id = public_id
        self.name =  name
        self.email = email
        self.password = password 

    def as_dict(self) : 
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}


class Post(db.Model) :

    __tablename__ = "post"

    id = db.Column(db.Integer , primary_key = True)
    userid = db.Column(db.Integer)  #foreign key
    image = db.Column(db.String(500))
    msg = db.Column(db.String(500))
    created_time = db.Column(db.DateTime)
    no_of_likes = db.Column(db.Integer)
    no_of_dislikes = db.Column(db.Integer) 

    def __init__(self , id, userid , image , msg , created_time , no_of_likes , no_of_dislikes) :
        self.id = id 
        self.userid = userid   # foreign key
        self.image = image
        self.msg = msg 
        self.created_time = created_time
        self.no_of_likes = no_of_likes
        self.no_of_dislikes = no_of_dislikes

    def as_dict(self) : 
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}


class Comment(db.Model) :

    __tablename__ = "comment" 

    id = db.Column(db.Integer , primary_key =True) 
    userid = db.Column(db.Integer) # foreign  key
    postid = db.Column(db.Integer) #foreign key
    msg = db.Column(db.String(100))
    created_time = db.Column(db.DateTime)

    def __init__(self , id , userid , postid , msg , created_time) :
        self.id = id
        self.userid = userid
        self.postid = postid
        self.msg = msg 
        self.created_time = created_time

    def as_dict(self) :
        return {c.name: str(getattr(self , c.name)) for c in self.__table__.columns}



