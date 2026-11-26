from flask_wtf import FlaskForm
from sqlalchemy import DateTime
from wtforms import StringField, PasswordField, IntegerField, FloatField, SelectField, SubmitField, DateField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo

class ProjectTypeForm(FlaskForm):
    type = SelectField('Project Type', choices=[('General', 'general'), ('Executable', 'executable'), ('Game', 'game')])
    submit = SubmitField('Select')


class GeneralForm(FlaskForm):
    name = StringField('Title', validators=[DataRequired(), Length(min=4, max=80)])
    description = StringField('Description', validators=[DataRequired(), Length(min=12, max=256)])
    tag = SelectField('Tag', choices=[('AI', 'ai'), ('System', 'system'), ('Game System', 'game system'), ('CAD', 'cad'), ('Animation', 'animation'), ('Electronics', 'electronics'), ('Robotics', 'robotics'), ('Engineering', 'engineering')])
    category = SelectField('Category', choices=[('Software', 'software'), ('Game', 'game'), ('Engineering', 'engineering'), ('General', 'general'), ('3D Design', '3d design')])
    tools = TextAreaField('Tools Used (one per line)')
    cover_image = TextAreaField('Cover Image')
    image_urls = TextAreaField('Image URLs')
    video_urls = TextAreaField('Video URLs')
    submit = SubmitField('Submit')


class ExecutableForm(FlaskForm):
    name = StringField('Title', validators=[DataRequired(), Length(min=4, max=80)])
    description = StringField('Description', validators=[DataRequired(), Length(min=12, max=256)])
    tag = SelectField('Tag', choices=[('AI', 'ai'), ('System', 'system'), ('Game System', 'game system'), ('CAD', 'cad'), ('Animation', 'animation'), ('Electronics', 'electronics'), ('Robotics', 'robotics'), ('Engineering', 'engineering')])
    category = SelectField('Category', choices=[('Software', 'software'), ('Game', 'game'), ('Engineering', 'engineering'), ('General', 'general'), ('3D Design', '3d design')])
    tools = TextAreaField('Tools Used (one per line)')
    submit = SubmitField('Submit')


class GameForm(FlaskForm):
    name = StringField('Title', validators=[DataRequired(), Length(min=4, max=80)])
    description = StringField('Description', validators=[DataRequired(), Length(min=12, max=256)])
    tag = SelectField('Tag', choices=[('AI', 'ai'), ('System', 'system'), ('Game System', 'game system'), ('CAD', 'cad'), ('Animation', 'animation'), ('Electronics', 'electronics'), ('Robotics', 'robotics'), ('Engineering', 'engineering')])
    category = SelectField('Category', choices=[('Software', 'software'), ('Game', 'game'), ('Engineering', 'engineering'), ('General', 'general'), ('3D Design', '3d design')])
    tools = TextAreaField('Tools Used (one per line)')
    html_url = StringField('HTML URL', validators=[DataRequired()])
    submit = SubmitField('Submit')


class EditForm(FlaskForm):
    name = StringField('Title', validators=[Length(min=4, max=80)])
    description = StringField('Description', validators=[Length(min=0, max=256)])
    tools = TextAreaField('Tools Used (one per line)')
    image_urls = TextAreaField('Image URLs')
    video_urls = TextAreaField('Video URLs')
    html_url = StringField('HTML URL')
    submit = SubmitField('Submit')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=80)])
    email = StringField('Email', validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired(), Length(min=6, max=256)])
    submit = SubmitField('Create Account')


class LoginForm(FlaskForm):
    username = StringField('Username')
    email = StringField('Email', validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class ContactForm(FlaskForm):
    name = StringField('Name')
    email = StringField('Email')
    message = StringField('Message')
    submit = SubmitField('Send')
