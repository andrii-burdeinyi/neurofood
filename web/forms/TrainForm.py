from wtforms import Form, StringField, validators

class TrainForm(Form):
    username = StringField('username', [validators.Length(min=2, max=25)])
