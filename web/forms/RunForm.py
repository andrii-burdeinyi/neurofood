from wtforms import Form, StringField, validators

class RunForm(Form):
    username = StringField('username', [validators.Length(min=2, max=25)])
