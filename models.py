from livraria import db

# class Livros(db.Model):
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     nome = db.Column(db.String(50), nullable=False)
   

class Genero(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(40), nullable=False)
    
    def __repr__(self):
        return 'Name %r' % self.nome


class Autor(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(50), nullable=False)
    
    def __repr__(self):
         return 'Name %r' % self.nome
     
class Livros(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(50), nullable=False)
    
    genero_id = db.Column(db.Integer, db.ForeignKey('genero.id'), nullable=False)
    autor_id = db.Column(db.Integer, db.ForeignKey('autor.id'), nullable=False)
    
    genero = db.relationship("Genero", backref="livros")
    autor = db.relationship("Autor", backref="livros")
    
    def __repr__(self):
         return f'Livro {self.nome}'

      