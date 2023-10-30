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
        self.data = generalTools.splitByEmptySpace(generalTools.getDate())[0]

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
            
    def getFileName(self, jsonData: dict):
        if jsonData['source']['generalLink']['params']['year'] != '':
            return f"{jsonData['source']['generalLink']['params']['namezip']}{jsonData['source']['generalLink']['params']['year']}{jsonData['source']['generalLink']['params']['month']}.zip"
        else:
            datas = pd.date_range(start="2021-01-01", end=self.data, freq='MS').strftime('%Y%m').tolist()
            return [f"{jsonData['source']['generalLink']['params']['namezip']}{data}.zip" for data in datas]

    def gettingMonthlyReturn(self, dados_fundos: pd.DataFrame):
        generalData = []
        for dados in dados_fundos:
            #data_inicio_mes = (dados['DT_COMPTC'].sort_values(ascending = True).unique())[0]
            #data_fim_mes = (dados['DT_COMPTC'].sort_values(ascending = True).unique())[-1]
            #generalData.append(dados[(dados['DT_COMPTC'].isin([data_inicio_mes, data_fim_mes]))])
            generalData.append(dados)
        return generalData
    
    def ajustingColumns(self, base_final: pd.DataFrame):
        base_final['DENOM_SOCIAL'] = base_final['DENOM_SOCIAL'].map(lambda x: generalTools.barToNull(generalTools.cleaningDataStr(x)), na_action='ignore')
        base_final['DT_COMPTC'] = pd.to_datetime(base_final['DT_COMPTC'])
        base_final = base_final.query('VL_TOTAL > 0 and VL_PATRIM_LIQ > 0 and VL_QUOTA > 0')

        base_final.reset_index(inplace=True)
        base_final = base_final.drop('index', axis=1)
        return base_final