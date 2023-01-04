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