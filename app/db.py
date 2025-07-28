import psycopg2
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=r"C:\Users\valbe\PycharmProjects\Financeiro\.env\init.env") # crie um arquivo init.env e digite dentro dele suas credenciais.

conexao = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    dbname=os.getenv("DB_BASEDADOS")
)

def criar_lancamentos(conexao):
    with conexao.cursor() as cursor:
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS lancamentos (id SERIAL PRIMARY KEY, data DATE, historico TEXT, valor INTEGER, conta TEXT)"
        )
    conexao.commit()

def listar_dados(conexao):
    with conexao.cursor() as cursor:
        cursor.execute(
            "SELECT * FROM lancamentos"
        )
        resultado = cursor.fetchall()
    print(resultado)

def inserir_dados_unicos(conexao, data, historico, valor, conta, tipo):
    query = "INSERT INTO lancamentos (data, historico, valor, conta, tipo) VALUES (%s, %s, %s, %s, %s)"
    with conexao.cursor() as cursor:
        cursor.execute(
            query,
            (data, historico, valor, conta, tipo)
        )
    conexao.commit()

def inserir_dados_multiplos(conexao, dados):
    query = "INSERT INTO lancamentos (data, historico, valor, conta) VALUES (%s, %s, %s, %s)"
    cursor = conexao.cursor()
    cursor.executemany(query, dados)
    conexao.commit()

def apagar_tudo(conexao):
    with conexao.cursor() as cursor:
        cursor.execute("""
        DROP TABLE lancamentos
        """)