import datetime
import time
import pandas as pd
import utils.logger_config as logger_config
import logging
import fastavro
from utils.tools import GeneralTools
from methods.extractors.webPageDataScrapers import WebPageDataScrapers

generalTools = GeneralTools()
webPageDataScrapers = WebPageDataScrapers()

logger_config.setup_logger(time.strftime("%Y-%m-%d %H:%M:%S"))

class TransformData:
    def __init__(self):
        pass

    def dfToExcel(self, df: pd.DataFrame, file_name: str, sheet_name='Sheet1'):
        df.to_excel(file_name, sheet_name=sheet_name, index=False)
        return df.to_excel()
    
    def dfToJson(self, df: pd.DataFrame, file_name: str):
        df.to_json(file_name, orient='records')
        return df.to_json()
    
    def dfToParquet(self, df: pd.DataFrame, file_name: str):
        df.to_parquet(file_name, index=False)
        return df.to_parquet()
    
    def df_to_pickle(self, df: pd.DataFrame, file_name: str):
        df.to_pickle(file_name)
        return df.to_pickle()
    
    def df_to_avro(self, df: pd.DataFrame, file_name: str):
        with open(file_name, 'wb') as out_avro:
            fastavro.writer(out_avro, df.to_dict(orient='records'))
        return df
    
    def df_to_html(self, df: pd.DataFrame, file_name: str):
        df.to_html(file_name, index=False)
        return df.to_html()

    def selectingData(self, df: pd.DataFrame, title: str, data: list):
        return df[df[title].isin(data)]
    
    def format_Date(self, date: str):
        try:
            return datetime.datetime.strptime(str(date), "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")
        except:
            return ""

    def cleaningDataRepeated(self, data: list):
        if data[-1] == data[-2]:
            data.pop()
        return data

    def cleaningEmptySpace(self, data: list, product):
        return list(filter(lambda item: item != '', data)) + [product]

    def deletingColumns(self, df: pd.DataFrame, diames: str):
        arg = str(datetime.datetime.strptime(diames, "%Y-%m-%d").strftime("%b/%y")).title()
        count = 2
        for f in range(0, len(df.columns)):
            if arg != df.iloc[0][-2]:
                df = df.drop(columns=df.columns[len(df.columns)-count:])
            elif arg == df.iloc[0][-2]:
                return df

    def ajustingFinalDataFrame(self, df: pd.DataFrame):
        novo_df = pd.DataFrame()
        novo_df['Situacao'] = df['Situacao'].map(lambda x: x.title())
        novo_df['Var_Desconto'] = df['Var_Desconto'].map(lambda x: int(generalTools.percentageToEmpty(x)))
        novo_df['Descricao'] = df['Descricao'].map(lambda x: f"'{generalTools.hyphenToEmptySpace(generalTools.plusToNull(generalTools.removeMinus(generalTools.removeParentheses(generalTools.removeEllipsis(x.replace('”',''))))))}'")
        novo_df['Codigo'] = df['Codigo'].map(lambda x: f"'{generalTools.splitByEmptySpace(x)[-1]}'")
        novo_df['Avaliacao'] = df['Avaliacao'].map(lambda x: generalTools.removeParentheses(x))
        novo_df['Preco_Original'] = df['Preco_Original'].map(lambda x: generalTools.replaceCommaToDot(generalTools.dotToEmpty(generalTools.removeEmptySpaceInStr(generalTools.brlToEmpty(x).replace("cada","")))))
        novo_df['Preco_A_Vista'] = df['Preco_A_Vista'].map(lambda x: generalTools.replaceCommaToDot(generalTools.dotToEmpty(generalTools.removeEmptySpaceInStr(generalTools.brlToEmpty(x).replace("cada","")))))
        novo_df['Produto'] = df['Produto'].map(lambda x: generalTools.hyphenToEmptySpace(x.title()))

        novo_df.reset_index(inplace=True)
        novo_df.drop('index', axis=1, inplace=True)
        return novo_df
