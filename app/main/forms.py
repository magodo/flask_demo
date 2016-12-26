from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField, PasswordField, SelectField, SelectMultipleField, BooleanField, TextAreaField, \
                    ValidationError
from wtforms.validators import Required, Length, Email, Optional, Regexp

from ..models import RoleModel, UserModel

#class LoginForm(FlaskForm):
#    name = StringField("User Name", validators = [Required()])
#    passwd = PasswordField("Password", validators = [Required()])
#    submit = SubmitField("Submit")
#
#class JoinForm(FlaskForm):
#
#    # mandatory
#    name = StringField("Name", validators=[Length(1,6,"Length should be <= 6")])
#    passwd = PasswordField("Passowrd", validators=[Required()])
#    email = StringField("E-mail", validators=[Required(), Email("Invalid E-mail address")])
#
#    # optional
#    phone = StringField("Phone Number", validators = [Optional(), Length(11, 11, "Invalid phone number")])
#    gender = SelectField("Gender", choices=[('M', 'Male'), ('F', 'Female')])
#    ##birthday = #TODO
#    company = StringField("Company")
#    job = SelectField("Job", choices=[('dev', 'Developer'), ('op', 'Operator')])
#    address = StringField("Address")
#    qq = StringField("QQ number")
#    # TODO: check how to specify HTML "row" attribute to the select field when rendering
#    #projs = SelectMultipleField("Project(s) involved", choices=[
#    #    ('p1', 'Project 1'), ('p2', 'Project 2'), ('p3', 'Project 3')])
#    submit = SubmitField("Submit")
#
#class ProfileForm(FlaskForm):
#
#    # mandatory
#    name = StringField("Name", validators=[Length(1,6,"Length should be <= 6")])
#    passwd = PasswordField("Passowrd", validators=[Required()])
#    email = StringField("E-mail", validators=[Required(), Email("Invalid E-mail address")])
#
#    # optional
#    phone = StringField("Phone Number", validators = [Optional(), Length(11, 11, "Invalid phone number")])
#    gender = SelectField("Gender", choices=[('M', 'Male'), ('F', 'Female')])
#    ##birthday = #TODO
#    company = StringField("Company")
#    job = SelectField("Job", choices=[('dev', 'Developer'), ('op', 'Operator')])
#    address = StringField("Address")
#    qq = StringField("QQ number")
#    # TODO: check how to specify HTML "row" attribute to the select field when rendering
#    #projs = SelectMultipleField("Project(s) involved", choices=[
#    #    ('p1', 'Project 1'), ('p2', 'Project 2'), ('p3', 'Project 3')])
#    submit = SubmitField("Submit")

###################
# Forms
###################

class EditProfileForm(FlaskForm):
    name = StringField('Username', validators=[Length(0, 64)])
    location = StringField('Location', validators=[Length(0, 64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')

class EditProfileAdminForm(FlaskForm):
    email = StringField("E-mail", validators=[Required(), Length(1,64),
                         Email("Invalid E-mail address")])
    name = StringField("Username", validators=[Required(), Length(1,6,
                        "User name should be less than 6 characters"),
                        Regexp('^[a-zA-Z][A-Za-z0-9_.]*$', 0, 'Username must have only letters, '
                        'numbers, dots or underscores and starts with letters.')])
    confirmed = BooleanField('Confirmed')
    role = SelectField('Role', coerce=int)
    location = StringField('Location', validators=[Length(0,64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name)
                             for role in RoleModel.query.order_by(RoleModel.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and \
                UserModel.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_name(self, field):
        if field.data != self.user.name and \
                UserModel.query.filter_by(name=field.data).first():
            raise ValidationError('Username already in use.')

