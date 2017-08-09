from flask_wtf import Form
from wtforms import TextField, IntegerField,SubmitField,RadioField,SelectField,StringField,PasswordField
from wtforms import validators, ValidationError

class NewAccount(Form):
    email = StringField("Email Address",[validators.Required("Please enter your email address."),
      validators.Email("Please enter your email address.")])
    userName = StringField("User screen Name",[validators.Required("Please enter Screen Name.")])
    Password = PasswordField("Password",[validators.Required("Please enter your password.")])



    FavoriteTeam = SelectField('Favorite Team',id='FavoriteTeam')
    Fname = StringField("First Name",[validators.Required("Please enter your first name.")])
    Lname = StringField("Last Name",[validators.Required("Please enter your last name.")])

    submit = SubmitField("Submit")



class Login(Form):
    email = StringField("Email Address", [validators.Required("Please enter your email address."),
                                          validators.Email("Please enter your email address.")])
    Password = PasswordField("Password", [validators.Required("Please enter your password.")])
    submit = SubmitField("Login")