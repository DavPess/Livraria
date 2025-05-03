from flask import Flask, render_template, request, redirect, session, flash, url_for
from livraria import app, db
from models import Autor, Genero, Livros as Livro
from helpers import FormularioAutor, FormularioGenero, FormularioLivro, FormularioLivros
import rota_index
import time

# criando cadastro de livros
@app.route("/livro")
def exibir_livro():
    mostrar_livro = Livro.query.all()
    livro = [{"id": livro.id, "livro": livro.nome} for livro in mostrar_livro]

    print(mostrar_livro)
    return render_template("livro/livro.html", livro=livro, active="livro")


@app.route("/livro/novo", methods=["POST", "GET"])
def novo_livro():
    form = FormularioLivro()
    print(form.validate_on_submit())
    form.genero.choices = [(g.id, g.nome) for g in Genero.query.all()]
    form.autor.choices = [(a.id, a.nome) for a in Autor.query.all()]
    if (
        request.method == "POST" and form.validate_on_submit()
    ):  # Verifica se o formulário foi enviado corretamente
        livro = form.nome.data.title()
        genero_id = form.genero.data
        autor_id = form.autor.data

        # Verifica se o livro já existe
        if Livro.query.filter_by(nome=livro).first():
            flash("Livro já existente!", "error")
            return render_template(
                "livro/novo_livro.html", titulo="Novo Livro", form=form
            )

        # Criando e salvando o novo livro
        novo_livro = Livro(nome=livro, genero_id=genero_id, autor_id=autor_id)
        db.session.add(novo_livro)
        db.session.commit()

        flash("Livro cadastrado com sucesso!", "success")
        return redirect(url_for("exibir_livro"))
    return render_template("livro/novo_livro.html", form=form)


@app.route("/livro/deletar/<int:id>")
def deletar_livro(id):
    Livro.query.filter_by(id=id).delete()  # Busca o livro pelo ID ou retorna erro 404
    db.session.commit()

    flash("Livro deletado com sucesso!")
    return redirect(url_for("exibir_livro"))


@app.route("/livro/atualizar/", methods=["POST"])
def atualizar_livro():
    livro = Livro.query.get(request.form["id"])
    # genero = Genero.query.get(request.form["id"])
    # autor = Autor.query.get(request.form["id"])

    form = FormularioLivro()
    form.genero.choices = [(g.id, g.nome) for g in Genero.query.all()]
    form.autor.choices = [(a.id, a.nome) for a in Autor.query.all()]

    if form.validate_on_submit():
        livro.nome = form.nome.data.title()
        livro.genero_id = form.genero.data
        livro.autor_id = form.autor.data

        db.session.commit()
        flash("Livro atualizado com sucesso!", "success")
        return redirect(url_for("exibir_livro"))
    else:
        flash("Erro ao atualizar o livro.", "danger")
        return redirect(url_for("editar_livro", id=livro.id))


@app.route("/livro/editar/<int:id>")
def editar_livro(id):
    livro = Livro.query.get_or_404(id)

    form = FormularioLivro()
    form.genero.choices = [(g.id, g.nome) for g in Genero.query.all()]
    form.autor.choices = [(a.id, a.nome) for a in Autor.query.all()]

    form.nome.data = livro.nome
    form.genero.data = livro.genero_id
    form.autor.data = livro.autor_id

    return render_template(
        "livro/editar_livro.html", titulo="Editando Cadastro de Livro", form=form, id=id
    )
