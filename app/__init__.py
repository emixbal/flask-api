from flask import Flask, request, jsonify
from flask_restplus import Resource, Api, fields
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost:3306/resep'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

from app.modules.catalogs import catalog
from app.modules.users import users



app.register_blueprint(users, url_prefix='/api/v1')
#app.register_blueprint(catalog, url_prefix='/v1')

db.create_all()
