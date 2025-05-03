from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_pyfile('config.py')

db = SQLAlchemy(app)

from rota_autor import *
from rota_genero import *
from rota_livro import *
from rota_index import *
if __name__ == '__main__':   
    app.run(debug=True)
