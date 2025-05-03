from flask import Flask, render_template, request, redirect, session, flash, url_for
from livraria import app, db
from models import Autor, Genero, Livros as Livro
from helpers import FormularioAutor, FormularioGenero, FormularioLivro, FormularioLivros

import time


@app.route("/")
def index():
    livros = Livro.query.all()

    livros_info = [
        {
            "nome": livro.nome,
            "genero": livro.genero.nome,
            "autor": livro.autor.nome
        }
        for livro in livros
    ]

    return render_template("index/index.html", livros=livros_info)