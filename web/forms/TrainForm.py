from wtforms import Form, StringField, validators
import wtforms_json


wtforms_json.init()


class TrainForm(Form):
    username = StringField('username', [validators.Length(min=2, max=25)])
