import pandas as pd
import pdfplumber as pl

def processar_extrato(caminho_pdf: str, nome_usuario: str):
    extrato = []

    with pl.open(caminho_pdf) as pdf:
        pag_principal = pdf.pages[1]

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
            historico = lancamento[6:posicao_valor-1]
            valor = lancamento[posicao_valor:].replace(",", ".")

            extrato.append((data, historico, valor))

        return pd.DataFrame(extrato, columns=["Data", "Historico", "Valor"])