import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from utils.tools import GeneralTools
generalTools = GeneralTools()

class GeneralCharts:
    def __init__(self):
        self.data = generalTools.getDate()

    def barChart(self, size: list, base_final: pd.DataFrame, duplicado: str, colref: str, title: str, xlab: str, ylab: str, xtick: int, data: str, nameDirectory: str):
        base_final = base_final.drop_duplicates(subset=duplicado)[colref].value_counts()
        plt.figure(figsize=(size[0], size[1]))
        plt.bar(pd.Series(base_final.index), pd.Series(base_final.values), color='skyblue')
        plt.title(f"{title} ({data})")
        plt.xlabel(xlab)
        plt.ylabel(ylab)
        plt.xticks(rotation=xtick)
        plt.yscale('log')
        plt.grid(axis='y', linestyle='--', alpha=1)
        for i, v in enumerate(base_final.values):
            plt.text(i, v + 0.5, str(v), ha='center')

        plt.tight_layout()
        plt.savefig(f"{nameDirectory}/DistribuicaoTiposFundos_{data}.png")
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

    def netAssetValueEvolution(self, size: list, base_final: pd.DataFrame, duplicado: str, colref: str, title: str, xlab: str, ylab: str, xtick: int, data: str, nameDirectory: str):
        # Converter a coluna 'DT_COMPTC' para o formato de data
        base_final['DT_COMPTC'] = pd.to_datetime(base_final['DT_COMPTC'])

        # Criar um gráfico de linha para mostrar a evolução do valor patrimonial líquido ao longo do tempo
        plt.figure(figsize=(size[0], size[1]))
        # Calcular o valor médio do patrimônio líquido para cada data e plotando
        base_final.groupby('DT_COMPTC')['VL_PATRIM_LIQ'].mean().plot()
        plt.title('Evolução do Valor Patrimonial Líquido ao Longo do Tempo')
        plt.xlabel('Data')
        plt.ylabel('Valor Patrimonial Líquido Médio')
        plt.show()