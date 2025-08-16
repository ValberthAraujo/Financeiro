import sqlite3

conn_sqlite = sqlite3.connect('cache.db')

def criar_tabela_lancamentos(conexao):
    cursor = conexao.cursor()
    cursor.execute("CREATE TABLE lancamentos (id PRIMARY KEY AUTOINCREMENT,  )")
