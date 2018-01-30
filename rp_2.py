# flask_marshmallow
# slqalchemy
from flask import Flask, request, jsonify
from flask_restplus import Resource, Api, fields
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
#flask admin
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
# Api
from flask_rest_jsonapi import Api, ResourceDetail, ResourceList, ResourceRelationship

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost:3306/tc'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'thisissecretkey'


api = Api(app)
db = SQLAlchemy(app)
ma = Marshmallow(app)

admin = Admin(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __init__(self, username=None, email=None):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username

class Reward(db.Model):
    id   = db.Column(db.Integer, primary_key=True)
    reward_name =  db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref='rewards')

class RewardSchema(ma.ModelSchema):
    class Meta:
        model = Reward

admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Reward, db.session))


@app.route('/')
def index():
    one_user = User.query.all()
    user_schema = UserSchema(many=True)
    output = user_schema.dump(one_user).data
    return jsonify({'user':output})

@api.route('/users')
class Language(Resource):
    # @api.marshal_with(a_language, envelope='lanhuages')
    def get(self):
        one_user = User.query.all()
        user_schema = UserSchema(many=True)
        output = user_schema.dump(one_user).data
        return jsonify({'user':output})



if __name__ == '__main__':
    app.run(debug=True, port=4000)
