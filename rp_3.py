# flask_marshmallow
# slqalchemy
from flask import Flask, request, jsonify, Blueprint
from flask_restplus import Resource, Api, fields
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

users = Blueprint('users', __name__, url_prefix='/api')
api = Api(users, doc='/doc')
app.register_blueprint(users)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost:3306/tc'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

from app.models.users_dua import User

class UserSchema(ma.ModelSchema):
    class Meta:
        model = User

a_user = api.model('User',
        {
            'email' : fields.String('email.'),
            'username' : fields.Integer('username')
        }
    )

@app.route('/')
def index():
    return 'hallo'

@api.route('/users')
class UserRest(Resource):
    def get(self):
        one_user = User.query.all()
        user_schema = UserSchema(many=True)
        output = user_schema.dump(one_user).data
        return jsonify({'user':output})

    @api.expect(a_user)
    def post(self):
        username = request.json.get('username')
        email = request.json.get('email')
        user = User(username=username, email=email)
        db.session.add(user)
        db.session.commit()
        return {'result':'User added.'}



if __name__ == '__main__':
    app.run(debug=True)
