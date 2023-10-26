import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from utils.tools import GeneralTools
import mplcursors

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

    def netAssetValueEvolution(self, size: list, base_final: pd.DataFrame, title: str, xlab: str, ylab: str, xtick: int, data: str, nameDirectory: str, fundos, cnpjs_fundos, patrimonio_liquido):

        # Configurar o gráfico
        fig, ax1 = plt.subplots(figsize=(size[0], size[1]))

        # Plotar os valores patrimoniais de cada CNPJ em relação às datas no eixo Y à direita
        for i, cnpj in enumerate(cnpjs_fundos):
            dados_cnpj = base_final[base_final['CNPJ_FUNDO'] == cnpj]
            line, = ax1.plot(dados_cnpj['DT_COMPTC'], dados_cnpj['VL_PATRIM_LIQ'], marker='o', linestyle='-', label=f'CNPJ: {cnpj}')

        ax1.set_xlabel(f'{xlab}')
        ax1.set_ylabel(f'{ylab}', color='black')
        ax1.tick_params(axis='y', labelcolor='black')
        ax1.legend(loc='best', bbox_to_anchor=(1, 1), title='Legenda')

        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.grid(axis='x', linestyle='--', alpha=0.7)

        # Rotacionar as datas para melhor visualização
        plt.xticks(rotation=xtick)

        # Adicionar rótulo ao gráfico
        plt.title(f'{title} ({data})')
        plt.tight_layout()

        # Adicionar tooltips usando mplcursors
        mplcursors.cursor(hover=True).connect("add", lambda sel: sel.annotation.set_text(f'Valor:   {sel.artist.get_ydata()[sel.target.index]}'))

        # Gravar o gráfico
        plt.savefig(f"{nameDirectory}/EvoluçãoPatr.Líq.MelhoresFundos_{data}.png")

        # Exibir o gráfico
        plt.show()