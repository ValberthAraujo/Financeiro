import pandas as pd

def converter_dados(caminho):
    df = pd.read_excel(caminho, header=1)
    df['DATA'] = df['DATA'].dt.strftime("%Y-%m-%d")
    valores = list(df.itertuples(index=False, name=None))
    print(valores)