from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, HiddenField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
# from assets.models import User

class NameForm(FlaskForm):
	name = StringField('Qual Seu Nome ', validators=[Length(min=2, max=30), DataRequired()])
	submit = SubmitField('Enviar')
	