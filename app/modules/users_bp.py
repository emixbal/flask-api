from flask import request, jsonify, Blueprint, abort
from flask.views import MethodView
from app import db, app
from app.models.users import Users


users = Blueprint('users', __name__)

@users.route('/users', methods=['GET'])
def get_users(id=None, page=1):
    users = Users.query.paginate(page, 10).items
    res = {}
    for user in users:
        res[user.id] = {
            'username': user.username,
            'name': user.name,
        }
    return jsonify(res)


@users.route('/users/<int:id>', methods=['GET'])
def get_users_detail(id, page=1):
    user = Users.query.filter_by(id=id).first()
    if not user:
        abort(404)
    res = {
       	'username': user.username,
        'name': user.name,
    }
    return jsonify(res)

@users.route('/users', methods=['POST'])
def user_new():
    username = request.form.get('username')
    name = request.form.get('name')

    user = Users(username, name)
    db.session.add(user)
    db.session.commit()
    return jsonify({user.id: {
        'username': user.username,
        'name': user.name,
    }})

@users.route('/users/<int:id>', methods=['DELETE'])
def user_delete(id):
    Users.query.filter_by(id=id).delete()
    db.session.commit()

    res = {'status' : 'succeed'}
    return jsonify(res)

@users.route('/users/<int:id>', methods=['PUT'])
def user_update(id):
    user = Users.query.get(id)
    user.username = request.form.get('username')
    user.name = request.form.get('name')
    db.session.commit()

    res = {
        'name': user.username,
        'name': user.name,
    }
    return jsonify(res)
