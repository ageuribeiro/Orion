from wtforms import Form, StringField, IntegerField

class RegistrationFormMember(Form):
    username = StringField('Username')
    email = StringField('Email')
    name = StringField('Name')
    age = StringField('Age')