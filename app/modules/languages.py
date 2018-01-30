from flask import Flask, request, Blueprint
from flask_restplus import Namespace, Resource, fields

api = Namespace('languages', description='list of languages arraoung the world')



a_language = api.model('Language',{'language' : fields.String('The languag.')})

languages = []
python = {'language':'python'}
languages.append(python)

@api.route('/todo')
class Todo(Resource):
    @api.marshal_with(person, envelope='resource')
    def get(self, **kwargs):
        return db_get_todo()  # Some function that queries the db

@api.route('/language')
class Language(Resource):
    def get(self):
        return languages

    @api.expect(a_language)
    def post(self):
        languages.append(api.payload)
        return {'result':'language added.'}