from wtforms import Form, validators, IntegerField
import wtforms_json

wtforms_json.init()


class RunForm(Form):
    user_id = IntegerField('user_id', [validators.DataRequired(), validators.NumberRange(min=1)])
    day_of_week = IntegerField('day_of_week', [validators.DataRequired(), validators.NumberRange(min=1, max=5)])
