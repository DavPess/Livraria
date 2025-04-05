import mysql.connector
from mysql.connector import errorcode

print("Conectando...")
try:
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="root"
    )
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Existe algo errado no nome de usuário ou senha")
    else:
        print(err)

cursor = conn.cursor()

cursor.execute("DROP DATABASE IF EXISTS `livraria`;")
cursor.execute("CREATE DATABASE `livraria`;")
cursor.execute("USE `livraria`;")

# Criando tabelas corrigidas
TABLES = {}

TABLES["Autor"] = ('''
    CREATE TABLE `autor` (
        `id` INT(11) AUTO_INCREMENT PRIMARY KEY,
        `nome` VARCHAR(50) NOT NULL
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
''')

TABLES["Genero"] = ('''
    CREATE TABLE `genero` (
        `id` INT(11) AUTO_INCREMENT PRIMARY KEY,
        `nome` VARCHAR(40) NOT NULL
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
''')

TABLES["Livros"] = ('''
    CREATE TABLE `livros` (
        `id` INT(11) AUTO_INCREMENT PRIMARY KEY,
        `titulo` VARCHAR(50) NOT NULL,
        `genero_id` INT NOT NULL,
        `autor_id` INT NOT NULL,
        FOREIGN KEY (`genero_id`) REFERENCES `genero`(`id`),
        FOREIGN KEY (`autor_id`) REFERENCES `autor`(`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
''')

for tabela_nome in TABLES:
    tabela_sql = TABLES[tabela_nome]
    try:
        print(f"Criando tabela {tabela_nome}: ", end="")
        cursor.execute(tabela_sql)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("Já existe")
        else:
            print(err.msg)
    else:
        print("OK")

# Inserindo autores
autor_sql = "INSERT INTO autor (nome) VALUES (%s)"
autores = [
    ("George R. R. Martin",),
    ("J. R. R. Tolkien",),
    ("William P. Young",),
    ("Machado de Assis",),
    ("Franz Kafka",),
    ("Guimaraes Rosa",),
    ("Clarice Lispector",),
    ("Manuel Bandeira",),
    ("Cora Coralina",),
    
]
cursor.executemany(autor_sql, autores)

# Inserindo gêneros
genero_sql = "INSERT INTO genero (nome) VALUES (%s)"
generos = [
    ("Romance",),
    ("Suspense",),
    ("Ficção Religiosa",),
    ("Conto",)
]
cursor.executemany(genero_sql, generos)

# Recuperando os IDs de autores e gêneros
cursor.execute("SELECT id, nome FROM autor")
autores_dict = {nome: id for id, nome in cursor.fetchall()}

cursor.execute("SELECT id, nome FROM genero")
generos_dict = {nome: id for id, nome in cursor.fetchall()}

# Inserindo livros com os IDs corretos




# Consultando os dados
cursor.execute("SELECT * FROM autor")
print(" ------------- Autores:  -------------")
for autor in cursor.fetchall():
    print(autor[1])

cursor.execute("SELECT * FROM genero")
print(" ------------- Gêneros:  -------------")
for genero in cursor.fetchall():
    print(genero[1])

cursor.execute("SELECT * FROM livros")
print(" ------------- Livros:  -------------")
for livro in cursor.fetchall():
    print(livro[1])

# Commitando as alterações
conn.commit()

cursor.close()
conn.close()