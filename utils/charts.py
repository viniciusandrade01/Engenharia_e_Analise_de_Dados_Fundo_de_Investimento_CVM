import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from utils.tools import GeneralTools
generalTools = GeneralTools()

class GeneralCharts:
    def __init__(self):
        self.data = generalTools.getDate()

    def createBoxChart(self, df: pd.DataFrame, column: str, size: list, title: str, colors: str):
        plt.figure(figsize=(size[0], size[1]))
        sns.boxplot(y=column, data=df, color=colors)
        plt.title(title)
        plt.show()

    def createChart(self, size: list, piores_produtos, grupo):
        plt.figure(figsize=(size[0], size[1]))
        for index, row in piores_produtos.iterrows():
            plt.text(row['Faixa_de_Preco'].mid, row['Metrica_Ruim'], f"{row['Produto'].split(' ')[-1]}: {row['Metrica_Ruim']:.2f}", ha='center', va='bottom')
        plt.bar(grupo['Faixa_de_Preco_Mid'], grupo['Metrica_Ruim'], width=0.08, alpha=0.7)
        plt.xlabel('Faixa de Preco')
        plt.ylabel('Metrica Ruim')
        plt.xticks(rotation=45)
        plt.title('Piores Produtos por Faixa de Preço e Produtos')

        # Convertendo os valores das faixas em strings para o rótulo do eixo x
        rotulos_faixas = [str(faixa) for faixa in grupo['Faixa_de_Preco']]
        plt.xticks(grupo['Faixa_de_Preco_Mid'], rotulos_faixas)

        plt.savefig(f"Produtos_{generalTools.hyphenToNull(generalTools.splitByEmptySpace(self.data)[0])}/Piores_Produtos_{generalTools.hyphenToNull(generalTools.splitByEmptySpace(self.data)[0])}.png")
        plt.show() 