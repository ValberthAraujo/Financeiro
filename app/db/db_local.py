import sqlite3

conexao_local = sqlite3.connect("memoria_aplicacao.db")

def criar_tabela(conexao) -> None:
    query = "CREATE TABLE lancamentos (id INTEGER PRIMARY KEY AUTOINCREMENT, data TIMESTAMP, historico TEXT, valor INTEGER, conta TEXT)"
    cursor = conexao.cursor()

    cursor.execute(query)

def inserir_dados_unicos_local(conexao, data: str, historico: str, valor: int, conta: str) -> None:
    query = "INSERT INTO lancamentos (data, historico, valor, conta) VALUES (?, ?, ?, ?)"
    cursor = conexao.cursor()

    cursor.execute(query, data, historico, valor, conta)
    conexao.commit()

def inserir_dados_multiplos_local(conexao, dados) -> None:
    query = "INSERT INTO lancamentos (data, historico, valor, conta) VALUES (?, ?, ?, ?)"
    cursor = conexao.cursor()

    cursor.executemany(query, dados)
    conexao.commit()
