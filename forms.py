from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class SignUpForm(FlaskForm):
    name = StringField('Name',
                       validators=[DataRequired(), Length(min=2, max=20)])
    email = EmailField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class SignInForm(FlaskForm):
    email = EmailField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])

    submit = SubmitField('Sign In')

class RecipeForm(FlaskForm):
    in_1 = StringField('Ingredient 01',
                       validators=[DataRequired(), Length(min=2)])
    in_2 = StringField('Ingredient 02')
    in_3 = StringField('Ingredient 03')
    in_4 = StringField('Ingredient 04')
    in_5 = StringField('Ingredient 05')
    in_6 = StringField('Ingredient 06')
    in_7 = StringField('Ingredient 07')
    in_8 = StringField('Ingredient 08')
    in_9 = StringField('Ingredient 09')
    in_10 = StringField('Ingredient 10')
    submit = SubmitField('Find Recipes')