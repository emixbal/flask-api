from app import db, ma



class Users(db.Model):
    id 			= db.Column(db.Integer, primary_key=True)
    username 	= db.Column(db.String(10))
    name 		= db.Column(db.String(30))

    def __init__(self, username, name):
        self.username = username
        self.name = name

    def __repr__(self):
        return '<Users %d>' % self.id

class UsersSchema(ma.ModelSchema):
    class Meta:
        model = Users
