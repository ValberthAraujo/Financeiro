import sqlite3
import pandas as pd
from app.db.db_local import inserir_dados_multiplos_local

bd_local = sqlite3.connect(r"C:\Users\valbe\PycharmProjects\Financeiro\app\db\memoria_aplicacao.db")


def converter_dados(caminho):
    df = pd.read_excel(caminho, header=1)
    df['DATA'] = df['DATA'].dt.strftime("%Y-%m-%d")
    valores = list(df.itertuples(index=False, name=None))

    inserir_dados_multiplos_local(bd_local, valores)