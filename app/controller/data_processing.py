import pandas as pd
import pdfplumber as pl
from pandas.core.window import Expanding

caminho = "../../example.pdf"

def processar_extrato(caminho_pdf: str, pag_index: int, nome_usuario: str):
    extrato = []

    with pl.open(caminho_pdf) as pdf:
        pag_principal = pdf.pages[pag_index]

        try:
            tabela_bruta = pag_principal.extract_table()[1][0].split("\n")
        except Exception:
            raise ValueError("Falha ao encontrar a tabela no seu arquivo.") from Exception

        ano = pdf.metadata.get('CreationDate')[2:6]

        for lancamento in tabela_bruta:
            if nome_usuario in lancamento or "Total" in lancamento:
                continue

            posicao_valor = len(lancamento) - lancamento[::-1].index(" ")

            data = f"{ano}-{lancamento[0:5].replace("/", "-")}"
            lancamento_principal = lancamento[6:posicao_valor-1]

            try:
                with lancamento[posicao_valor:] as valor_inicial:
                    if "," in valor_inicial:
                        valor = valor_inicial.replace(",", ".")
                    else:
                        valor = valor_inicial
            except:
                valor = "0.00"


            extrato.append((data, lancamento_principal, valor))
    return extrato

print(processar_extrato(caminho, 1, "VALBERTH"))