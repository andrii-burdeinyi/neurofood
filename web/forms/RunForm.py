from wtforms import Form, validators, IntegerField
import wtforms_json

wtforms_json.init()

class RunForm(Form):
    user_id = IntegerField('userId', [validators.DataRequired(), validators.NumberRange(min=1)])
    day_of_week = IntegerField('dayOfWeek', [validators.DataRequired(), validators.NumberRange(min=1, max=5)])
