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
        
    def createBarhChart(self, size: list, fundos, cnpjs_fundos, patrimonio_liquido, data, nameDirectory, toprange):
        # Criando o gráfico de barras horizontais
        plt.figure(figsize=(size[0], size[1]))
        plt.barh(cnpjs_fundos, patrimonio_liquido, color='green')
        plt.xlabel('Patrimônio Líquido (R$)')
        plt.ylabel('Fundos de Investimento')
        plt.title(f"Top {toprange} Fundos de Investimento ({data})")
        plt.yticks(cnpjs_fundos, rotation='horizontal')
        plt.grid(axis='x', linestyle='--', alpha=0.7)

        # Adicionando os CNPJs aos rótulos das barras
        for index, value in enumerate(patrimonio_liquido):
            #plt.text(value, index, f' Patrim. Líq.: {list(cnpjs_fundos)[index]}', va='center')
            plt.text(value, index, f' Patrimônio Líquido: {value}', va='center')

        plt.tight_layout()
        plt.savefig(f"{nameDirectory}/MelhoresFundos_{data}.png")
        plt.show() 

    def createChart(self, size: list, nomes_fundos, cinco_maiores_valores, valores_cota, cnpjs_fundos):
        # Cria o gráfico de barras
        plt.figure(figsize=(size[0], size[1]))
        bars = plt.bar(nomes_fundos, cinco_maiores_valores, color='skyblue')

        # Adiciona o nome do fundo ao passar o mouse sobre a barra
        plt.xticks(rotation=45, ha='right')
        plt.ylabel('Valor do Patrimônio Líquido')

        # Adiciona os rótulos em cima das barras
        plt.bar_label(bars, labels=[f'{valor:.2f}\n{cnpj}\n{nome}' for valor, cnpj, nome in zip(cinco_maiores_valores, cnpjs_fundos, nomes_fundos)], 
                    label_type='edge', fontsize=8)

        # Adiciona o valor da cota e o nome do fundo sobre cada barra
        #for i, valor in enumerate(cinco_maiores_valores):
        #    plt.text(i, valor + 0.1, f'Valor: {valor}\nCota: {valores_cota.iloc[i]}', ha='center')

        plt.xlabel('Nome do Fundo')
        plt.title('5 Maiores Valores de Patrimônio Líquido')
        plt.tight_layout()
        plt.savefig(f"bla.png")
        plt.show() 