# flask_marshmallow
# slqalchemy
from flask import Flask, request, jsonify, Blueprint
from flask_restplus import Resource, Api, fields
from app import db, app, ma
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

from app.models.users import Users, UsersSchema


users = Blueprint('users', __name__)
api = Api(users, doc='/doc')

# expect for swagger post body input
post_body = api.model('User', {
    'name' : fields.String('name'),
    'username' : fields.Integer('username')
})

@app.route('/')
def index():
    return 'hallo'

@api.route('/users')
class UserList(Resource):
    def get(self):
        users = Users.query.all()
        users_schema = UsersSchema(many=True)
        output = users_schema.dump(users).data
        return jsonify(output)

    @api.expect(post_body)
    def post(self):
        name = request.json.get('name')
        username = request.json.get('username')
        user = Users(name=name, username=username)
        db.session.add(user)
        db.session.commit()
        return {'result':'User added.'}

@api.route('/users/<int:id>')
class UserDetail(Resource):
    def get(self, id):
        one_user = Users.query.filter_by(id=id).first()
        users_schema = UsersSchema()
        output = users_schema.dump(one_user).data
        return jsonify(output)

    def delete(self, id):
        Users.query.filter_by(id=id).delete()
        db.session.commit()
        return {'status' : 'succeed'}

if __name__ == '__main__':
    app.run(debug=True)
