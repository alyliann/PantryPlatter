from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, EmailField
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
    in_1 = StringField('Ingredient 1',
                       validators=[DataRequired(), Length(min=2)])
    in_2 = StringField('Ingredient 2',
                       validators=[Length(min=2)])
    in_3 = StringField('Ingredient 3',
                       validators=[Length(min=2)])
    in_4 = StringField('Ingredient 4',
                       validators=[Length(min=2)])
    in_5 = StringField('Ingredient 5',
                       validators=[Length(min=2)])
    in_6 = StringField('Ingredient 6',
                       validators=[Length(min=2)])
    in_7 = StringField('Ingredient 7',
                       validators=[Length(min=2)])
    in_8 = StringField('Ingredient 8',
                       validators=[Length(min=2)])
    in_9 = StringField('Ingredient 9',
                       validators=[Length(min=2)])
    in_10 = StringField('Ingredient 10',
                       validators=[Length(min=2)])
    submit = SubmitField('Find Recipes')