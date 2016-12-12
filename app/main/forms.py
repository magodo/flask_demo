from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField, PasswordField, SelectField, SelectMultipleField
from wtforms.validators import Required, Length, Email, Optional

class LoginForm(FlaskForm):
    name = StringField("User Name", validators = [Required()])
    passwd = PasswordField("Password", validators = [Required()])
    submit = SubmitField("Submit")

class JoinForm(FlaskForm):

    # mandatory
    name = StringField("Name", validators=[Length(1,6,"Length should be <= 6")])
    passwd = PasswordField("Passowrd", validators=[Required()])

    # optional
    phone = StringField("Phone Number", validators = [Optional(), Length(11, 11, "Invalid phone number")])
    mail = StringField("E-mail", validators=[Optional(), Email("Invalid E-mail address")])
    gender = SelectField("Gender", choices=[('M', 'Male'), ('F', 'Female')])
    ##birthday = #TODO
    company = StringField("Company")
    job = SelectField("Job", choices=[('dev', 'Developer'), ('op', 'Operator')])
    address = StringField("Address")
    qq = StringField("QQ number")
    # TODO: check how to specify HTML "row" attribute to the select field when rendering
    #projs = SelectMultipleField("Project(s) involved", choices=[
    #    ('p1', 'Project 1'), ('p2', 'Project 2'), ('p3', 'Project 3')])
    submit = SubmitField("Submit")

class ProfileForm(FlaskForm):

    # mandatory
    name = StringField("Name", validators=[Length(1,6,"Length should be <= 6")])
    passwd = PasswordField("Passowrd", validators=[Required()])
    # optional
    phone = StringField("Phone Number", validators = [Optional(), Length(11, 11, "Invalid phone number")])
    mail = StringField("E-mail", validators=[Optional(), Email("Invalid E-mail address")])
    gender = SelectField("Gender", choices=[('M', 'Male'), ('F', 'Female')])
    ##birthday = #TODO
    company = StringField("Company")
    job = SelectField("Job", choices=[('dev', 'Developer'), ('op', 'Operator')])
    address = StringField("Address")
    qq = StringField("QQ number")
    # TODO: check how to specify HTML "row" attribute to the select field when rendering
    #projs = SelectMultipleField("Project(s) involved", choices=[
    #    ('p1', 'Project 1'), ('p2', 'Project 2'), ('p3', 'Project 3')])
    submit = SubmitField("Submit")
