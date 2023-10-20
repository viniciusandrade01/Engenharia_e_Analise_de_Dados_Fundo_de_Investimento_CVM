import fastavro
import pandas as pd
import utils.logger_config as logger_config
from utils.tools import GeneralTools
from methods.transformers.transformData import TransformData
import logging
from utils.charts import GeneralCharts
generalCharts = GeneralCharts()
generalTools = GeneralTools()
transformData = TransformData()
logger_config.setup_logger(generalTools.getDate())

class FileSavers:
    def __init__(self):
        pass

    def openingSheets(self, directory: str, sheet: str, rows: int, footer: int):
        return pd.read_excel(f"{directory}", sheet_name=f"{sheet}", skiprows=rows, skipfooter=footer)

    def generateFile(self, novo_df: pd.DataFrame, file_type, diretorio, sep, fileName, columnsList: list, ofertas):

        novo_df = novo_df[columnsList]

        generalTools.makeDirectory(diretorio)
        diretorio = f"{diretorio}/{fileName}"

        if ofertas != "":
            novo_df = novo_df[novo_df['Situacao'] == 'Oferta']
    
        novo_df = novo_df.reset_index()
        novo_df.drop("index", axis=1, inplace=True)

        #generalCharts.createBoxChart(novo_df, 'Preco_Original', [8, 6], 'Gráfico de Caixa - Preço Original', 'blue')

        #createBoxChart(novo_df, 'Preco_A_Vista', [8, 6], 'Gráfico de Caixa - Preço à Vista', 'orange')

        if file_type == 'csv':
            novo_df.to_csv(f"{diretorio}.csv", sep=f"{sep}", index=False)
            logging.info(f"DATAFRAME SALVO COMO {fileName} EM FORMATO CSV.") 
            return
        
        elif file_type == 'excel':
            novo_df.to_excel(f"{diretorio}.xlsx", index=False)
            logging.info(f"DATAFRAME SALVO COMO {fileName} EM FORMATO EXCEL.")
            return
        
        elif file_type == 'json':
            novo_df.to_json(f"{diretorio}.json", orient='records')
            logging.info(f"DATAFRAME SALVO COMO {fileName} EM FORMATO JSON.")
            return
        
        elif file_type == 'parquet':
            novo_df.to_parquet(f"{diretorio}.parquet", index=False)
            logging.info(f"DATAFRAME SALVO COMO {fileName} EM FORMATO PARQUET.")
            return
        
        elif file_type == 'hdf':
            novo_df.to_hdf(f"{diretorio}.h5", key='data')
            logging.info(f"DATAFRAME SALVO COMO {fileName} EM FORMATO HDF5/H5.")
            return
        
        elif file_type == 'pickle':
            novo_df.to_pickle(f"{diretorio}.pkl")
            logging.info(f"DATAFRAME SALVO COMO {fileName} EM FORMATO PICKLE.")
            return
        
        elif file_type == 'feather':
            novo_df.to_feather(f"{diretorio}.feather")
            logging.info(f"DATAFRAME SALVO COMO {fileName} EM FORMATO FEATHER.")
            return
        
        elif file_type == 'avro':
            with open(f"{diretorio}.avro", 'wb') as out_avro:
                fastavro.writer(out_avro, novo_df.to_dict(orient='records'))
            logging.info(f"DATAFRAME SALVO COMO {fileName} EM FORMATO AVRO.")
            return
        
        elif file_type == 'html':
            novo_df.to_html(f"{diretorio}.html", index=False)
            logging.info(f"DATAFRAME SALVO COMO {fileName} EM FORMATO HTML.")
            return
        
        else:
            logging.info("TIPO DE ARQUIVO NÃO SUPORTADO. ESCOLHA UM FORMATO VÁLIDO.")

    def concatDataFrame(self, df: pd.DataFrame, dictionary: dict, index: int):
        try:
            return pd.concat([df, pd.DataFrame(dictionary, index=[index])])
        except KeyError as e:
            logging.error(f"ERRO: {e}, A CHAVE {e} NÃO FOI ENCONTRADA NO DICIONÁRIO.")
        except Exception as e:
            logging.error(f"ERRO: {e}, NÃO FOI POSSÍVEL CONCATENAR OS DATAFRAMES.")

    def readDeepData(self, zip_file):
        return pd.read_csv(zip_file.open(zip_file.namelist()[0]), sep=";", encoding="ISO-8859-1")

    def readRegistrationData(self):
        dados_cadastro = pd.read_csv('https://dados.cvm.gov.br/dados/FI/CAD/DADOS/cad_fi.csv', sep=";", encoding="ISO-8859-1")

        dados_cadastro = dados_cadastro[['CNPJ_FUNDO', 'DENOM_SOCIAL']]

        dados_cadastro = dados_cadastro.drop_duplicates()
        return dados_cadastro
    
    def mergeDataFrames(self, dados_fundos_filtrado, dados_cadastro):
        base_final = pd.DataFrame()
        for fundos_filtrados in dados_fundos_filtrado:
            merged_df = pd.merge(fundos_filtrados, dados_cadastro, how="left", left_on =["CNPJ_FUNDO"], right_on = ["CNPJ_FUNDO"])
            base_final = pd.concat([base_final, merged_df], ignore_index=True)

        return base_final[['CNPJ_FUNDO', 'DENOM_SOCIAL', 'TP_FUNDO', 'DT_COMPTC', 'VL_TOTAL', 'VL_QUOTA', 'VL_PATRIM_LIQ', 'NR_COTST']]
    
    def gettingTheBestInvestmentFunds(self, base_final: pd.DataFrame, range: int):
        # Usando, como referência e parâmetro, o último dia como dia 30, e removendo duplicados
        base_final = base_final[pd.to_datetime(base_final['DT_COMPTC']).dt.day == 30]

        # Coletando os 'range' maiores valores, usando como referência o Patrimônio Líquido
        maiores_valores = base_final['VL_PATRIM_LIQ'].nlargest(range)
        nomes_fundos = base_final.loc[maiores_valores.index, 'DENOM_SOCIAL']
        valores_cota = base_final.loc[maiores_valores.index, 'VL_QUOTA']
        cnpjs_fundos = base_final.loc[maiores_valores.index, 'CNPJ_FUNDO']
        
        return maiores_valores, nomes_fundos, valores_cota, cnpjs_fundos