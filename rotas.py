from flask import Flask, render_template, request, redirect, session, flash, url_for
from livraria import app, db
from models import Autor, Genero
from helpers import  FormularioAutor, FormularioGenero
import time



#Cadastro de autores

@app.route("/")
def index():
    return redirect(url_for('exibir_autor'))
 
@app.route("/autor")
def exibir_autor():
    mostrar_autor = Autor.query.all()
    autores = [{"id": autor.id, "autor": autor.nome} for autor in mostrar_autor]

    return render_template("autor/autor.html", autores=autores, active="autor")

@app.route("/autor/novo", methods=["POST", "GET"])
def novo_autor():
    form = FormularioAutor()
    if (
        request.method == "POST" and form.validate_on_submit()
    ):  # Verifica se o formulário foi enviado corretamente
        autor = form.autor.data.title()

        # Verifica se o autor já existe
        if Autor.query.filter_by(nome=autor).first():
            flash("Autor já existente!", "error")
            return render_template("autor/novo_autor.html", titulo="Novo autor", form=form)

        # Criando e salvando o novo autor
        novo_autor = Autor(nome=autor)
        db.session.add(novo_autor)
        db.session.commit()

        flash("Autor cadastrado com sucesso!", "success")
        return redirect(url_for("exibir_autor"))
    return render_template("autor/novo_autor.html", form=form)


@app.route("/autor/deletar/<int:id>")
def deletar_autor(id):
    Autor.query.filter_by(
        id=id
    ).delete()  # Busca o livro pelo ID ou retorna erro 404
    db.session.commit()

    flash("Autor deletado com sucesso!")
    return redirect(url_for("exibir_autor"))

@app.route("/autor/atualizar/", methods=['POST'])
def atualizar_autor():
    autor = Autor.query.get(request.form["id"])
  
    if autor:
        autor.nome = request.form['autor']
        db.session.commit()
        flash("Autor(a) atualizado com sucesso!", "success")
    else:
        flash("Erro ao atualizar o Autor(a)!", "danger")

    return redirect(url_for("exibir_autor"))


@app.route("/autor/editar/<int:id>")
def editar_autor(id):
    autor = Autor.query.get_or_404(id)
    

    form = FormularioAutor()
    form.autor.data = autor.nome
   

    return render_template("autor/editar_autor.html", titulo="Editando autor", form=form, id=id)

#Cadastro de gênero literário

@app.route('/genero')
def exibir_genero():
    mostrar_genero = Genero.query.all()
    genero = [{"id": genero.id, "genero": genero.nome} for genero in mostrar_genero]

    return render_template("genero/genero.html", genero=genero, active="genero")

@app.route("/genero/novo", methods=["POST", "GET"])
def novo_genero():
    form = FormularioGenero()
    if (
        request.method == "POST" and form.validate_on_submit()
    ):  # Verifica se o formulário foi enviado corretamente
        genero = form.genero.data.title()

        # Verifica se o genero já existe
        if Genero.query.filter_by(nome=genero).first():
            flash("Gênero Literário já existente!", "error")
            return render_template("genero/novo_genero.html", titulo="Novo Gênero", form=form)

        # Criando e salvando o novo genero
        novo_genero = Genero(nome=genero)
        db.session.add(novo_genero)
        db.session.commit()

        flash("Gênero Literário cadastrado com sucesso!", "success")
        return redirect(url_for("exibir_genero"))
    return render_template("genero/novo_genero.html", form=form)

@app.route("/genero/deletar/<int:id>")
def deletar_genero(id):
    Genero.query.filter_by(
        id=id
    ).delete()  # Busca o genero pelo ID ou retorna erro 404
    db.session.commit()

    flash("Gênero Literário deletado com sucesso!")
    return redirect(url_for("exibir_genero"))

@app.route("/genero/atualizar/", methods=['POST'])
def atualizar_genero():
    genero = Genero.query.get(request.form["id"])
  
    if genero:
        genero.nome = request.form['genero']
        db.session.commit()
        flash("Gênero Literário atualizado com sucesso!", "success")
    else:
        flash("Erro ao atualizar o Gênero Liteário!", "danger")

    return redirect(url_for("exibir_genero"))

@app.route("/genero/editar/<int:id>")
def editar_genero(id):
    genero = Genero.query.get_or_404(id)
    

    form = FormularioGenero()
    form.genero.data = genero.nome
   

    return render_template("genero/editar_genero.html", titulo="Editando Gênero Literário", form=form, id=id)