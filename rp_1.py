# with marshal and marshmallow
from flask import Flask, request
from flask_restplus import Resource, Api, fields
from marshmallow import Schema, fields as ma_fields, post_load

app = Flask(__name__)
api = Api(app)

class TheLanguage(object):
    def __init__(self, language, framework):
        self.language = language
        self.framework = framework

    def __repr__(self):
        return '{} is the language. {} is the framework'.format(self.language, self.framework)

class LanguagesSchema(Schema):
    language = ma_fields.String()
    framework = ma_fields.String()

    @post_load
    def create_language(self, data):
        return TheLanguage(**data)

a_language = api.model('Language',
    {
        'language' : fields.String('The language.'),
        'framework' : fields.String('The framework.')
    }
)

languages = []
python = TheLanguage(language='python', framework='Django')
languages.append(python)


@api.route('/language')
class Language(Resource):
    def get(self):
        schema = LanguagesSchema(many=True)
        return schema.dump(languages)

    @api.expect(a_language)
    def post(self):
        schema = LanguagesSchema()

        new_language = schema.load(api.payload)
        languages.append(new_language.data)

        return {'result':'language added.'}


if __name__ == '__main__':
    app.run(debug=True)
