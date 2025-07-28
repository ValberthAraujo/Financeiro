import pandas as pd
from app.db import inserir_dados_multiplos, conexao

def converter_dados(caminho):
    df = pd.read_excel(caminho, header=1)
    valores = list(df.itertuples(index=False, name=None))
    inserir_dados_multiplos(conexao, valores)