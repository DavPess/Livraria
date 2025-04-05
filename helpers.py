import os
from livraria import app
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators, SelectField
from wtforms.validators import DataRequired, Length

class FormularioLivro(FlaskForm):
    titulo = StringField("Título", validators=[DataRequired()])
    genero = SelectField("Gênero", choices=[], coerce=int, validators=[DataRequired()])
    autor = SelectField("Autor(a)", choices=[], coerce=int, validators=[DataRequired()])
    salvar = SubmitField("Salvar")
    
class FormularioAutor(FlaskForm):
    autor = StringField("Autor", validators=[DataRequired()])
    salvar = SubmitField("Salvar")

class FormularioGenero(FlaskForm):
    genero = StringField("Genero", validators=[DataRequired()])
    salvar = SubmitField("Salvar")