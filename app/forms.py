from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, URL 

class GravadoraForm (FlaskForm):
    nome = StringField('Nome: ', validators=[DataRequired()])
    endereco = StringField('Endereço: ')
    telefone = StringField('Telefone: ')
    site = StringField('Site: ', validators=[URL()])
    contato = StringField('Contato: ')
    submit = SubmitField('Salvar')
