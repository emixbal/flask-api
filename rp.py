# tanpa Marshmallow
from flask import Flask, request
from flask_restplus import Resource, Api, fields

from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost:3306/resep'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

api = Api(app)


a_language = api.model('Language',
        {
            'language' : fields.String('The language.'),
            'id' : fields.Integer('Id')
        }
    )

languages = []
python = {'language':'python', 'id':1}
languages.append(python)


@api.route('/language')
class Language(Resource):
    @api.marshal_with(a_language, envelope='lanhuages')
    def get(self):
        return languages

    @api.expect(a_language)
    def post(self):
        new_language = api.payload
        new_language['id'] = len(languages)+1
        languages.append(new_language)
        return {'result':'language added.'}


if __name__ == '__main__':
    app.run(debug=True)
