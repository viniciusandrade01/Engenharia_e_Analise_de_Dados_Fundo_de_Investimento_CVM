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
    
    def dfToCsv(self, df: pd.DataFrame, file_name: str, separator: str):
        df.to_csv(file_name, sep=separator, index=False)
        logging.info("CONVERSÃO DO DATAFRAME PARA TIPO EXCEL REALIZADA COM SUCESSO.")
        return df.to_csv()

    def dfToExcel(self, df: pd.DataFrame, file_name: str, sheet_name='Sheet1'):
        df.to_excel(file_name, sheet_name=sheet_name, index=False)
        logging.info("CONVERSÃO DO DATAFRAME PARA TIPO EXCEL REALIZADA COM SUCESSO.")
        return df.to_excel()
    
    def dfToJson(self, df: pd.DataFrame, file_name: str):
        df.to_json(file_name, orient='records')
        logging.info("CONVERSÃO DO DATAFRAME PARA TIPO JSON REALIZADA COM SUCESSO.")
        return df.to_json()
    
    def dfToParquet(self, df: pd.DataFrame, file_name: str):
        df.to_parquet(file_name, index=False)
        logging.info("CONVERSÃO DO DATAFRAME PARA TIPO PARQUET REALIZADA COM SUCESSO.")
        return df.to_parquet()
    
    def df_to_pickle(self, df: pd.DataFrame, file_name: str):
        df.to_pickle(file_name)
        logging.info("CONVERSÃO DO DATAFRAME PARA TIPO PICKLE REALIZADA COM SUCESSO.")
        return df.to_pickle()
    
    def df_to_avro(self, df: pd.DataFrame, file_name: str):
        with open(file_name, 'wb') as out_avro:
            fastavro.writer(out_avro, df.to_dict(orient='records'))
            logging.info("CONVERSÃO DO DATAFRAME PARA TIPO AVRO REALIZADA COM SUCESSO.")
        return df
    
    def df_to_html(self, df: pd.DataFrame, file_name: str):
        df.to_html(file_name, index=False)
        logging.info("CONVERSÃO DO DATAFRAME PARA TIPO HTML REALIZADA COM SUCESSO.")
        return df.to_html()

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
        aux_base = base_final
        # Usando, como referência e parâmetro, o último dia como dia 30, e removendo duplicados
        base_final = base_final[pd.to_datetime(base_final['DT_COMPTC']).dt.day == 30]

        # Coletando os 'range' maiores valores, usando como referência o Patrimônio Líquido
        maiores_valores = base_final['VL_PATRIM_LIQ'].nlargest(range)
        nomes_fundos = base_final.loc[maiores_valores.index, 'DENOM_SOCIAL']
        valores_cota = base_final.loc[maiores_valores.index, 'VL_QUOTA']
        cnpjs_fundos = base_final.loc[maiores_valores.index, 'CNPJ_FUNDO']
        
        return maiores_valores, nomes_fundos, valores_cota, cnpjs_fundos, maiores_valores.index, aux_base[aux_base['DENOM_SOCIAL'].isin(nomes_fundos)].index