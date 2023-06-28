from flask import render_template, request
from models import User, Member
from forms import RegistrationFormMember


def register_member():
    form  = RegistrationFormMember(request.form)
    if request.method == 'POST' and form.validate():
        username = form.username.data
        email = form.email.data
        name = form.name.data
        age = form.age.data

        # Crie um novo membro no banco de dados ou faça qualquer outra ação

        return render_template('membros/success.html', member=member)

    return render_template('membros/add_member.html', form=form)
