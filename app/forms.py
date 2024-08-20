from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length


class LoginForm(FlaskForm):
    email = StringField('Correo:', validators=[DataRequired(), Email()])
    username = StringField('Nombre:', validators=[DataRequired()])
    password = PasswordField('Contraseña:', validators=[DataRequired()])
    submit = SubmitField('Login')


class SignupForm(FlaskForm):
    username = StringField('Nombre:', validators=[
                           DataRequired(), Length(min=2, max=20)])
    email = StringField('Correo:', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña:', validators=[DataRequired()])
    confirm_password = PasswordField('Confirmar Contraseña:', validators=[
                                     DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


class QuestionForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Submit')


class AnswerForm(FlaskForm):
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Submit')
