from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import SubmitField
from wtforms.validators import DataRequired


class TaskForm(FlaskForm):
    answer = StringField('Ответ')
    submit = SubmitField('Ответить')
