from flask import Flask, render_template, request, redirect, session, flash, url_for
from livraria import app, db
from models import Autor
from helpers import  FormularioAutor



@app.route("/autor")
def exibir_autor():
    mostrar_autor = Autor.query.all()
    autores = [{"id": autor.id, "autor": autor.nome} for autor in mostrar_autor]

    return render_template("autor.html", autores=autores, active="autor")

@app.route("/autor/novo", methods=["POST", "GET"])
def novo_autor():
    form = FormularioAutor()
    if (
        request.method == "POST" and form.validate_on_submit()
    ):  # Verifica se o formulário foi enviado corretamente
        autor = form.autor.data

        # Verifica se o autor já existe
        if Autor.query.filter_by(nome=autor).first():
            flash("Autor já existente!", "error")
            return render_template("novo_autor.html", titulo="Novo autor", form=form)

        # Criando e salvando o novo autor
        novo_autor = Autor(nome=autor)
        db.session.add(novo_autor)
        db.session.commit()

        flash("Autor cadastrado com sucesso!", "success")
        return redirect(url_for("exibir_autor"))
    return render_template("novo_autor.html", form=form)


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
   

    return render_template("editar_autor.html", titulo="Editando autor", form=form, id=id)