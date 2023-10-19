import os
import pandas as pd
import requests as rq
from methods.loaders.filesSave import FileSavers
from methods.transformers.transformData import TransformData
from methods.extractors.webPageDataScrapers import WebPageDataScrapers
from utils.tools import GeneralTools
#from utils.driver import DriverChrome
#from utils.selenium import GeneralSelenium
#from utils.selenium import GeneralSelenium
import utils.logger_config as logger_config
from utils.charts import GeneralCharts 
from utils.aws import AboutAWS
import logging

def main():
    try:
        fileSavers = FileSavers()
        transformData = TransformData()
        webPageDataScrapers = WebPageDataScrapers()
        generalTools = GeneralTools()
        generalCharts = GeneralCharts()
        #driverChrome = DriverChrome()
        #selenium = GeneralSelenium()
        df = pd.DataFrame()
        client = AboutAWS()
        # Variável contendo informações das moedas a serem coletadas, aws e banco de dados
        jsonData = generalTools.openJson()
        logger_config.setup_logger(generalTools.getDate())
        
        # CONFIGURANDO PARA 4 CASAS DECIMAIS A FORMATAÇÃO E EXIBIÇÃO DOS N°S DE PONTO FLUTUANTE 
        pd.options.display.float_format = '{:.4f}'.format

        name_directory = f"{jsonData['source']['generalLink']['params']['directory']}{generalTools.hyphenToNull(generalTools.splitByEmptySpace(generalTools.getDate())[0])}"
        name_file = f"inf_diario_fi_{jsonData['source']['generalLink']['params']['year']}{jsonData['source']['generalLink']['params']['month']}.zip"
        generalTools.makeDirectory(name_directory)

        html, soup = webPageDataScrapers.requestGetDefault(f"{jsonData['source']['generalLink']['url']}{name_file}")
        webPageDataScrapers.downloadUrl(html, name_file, name_directory)
        webPageDataScrapers.downloadUrlGroup(html, name_file, name_directory)
        zip_file = webPageDataScrapers.readZipFile(name_file, name_directory)
        logging.info("INFORMAÇÕES DA URL BAIXADA COM SUCESSO.")

        dados_fundos = fileSavers.readDeepData(zip_file)
        dados_cadastro = fileSavers.readRegistrationData()
        dados_fundos_filtrado = transformData.gettingMonthlyReturn(dados_fundos)
        base_final = fileSavers.mergeDataFrames(dados_fundos_filtrado, dados_cadastro)
        cinco_maiores_valores, nomes_fundos, valores_cota, cnpjs_fundos = fileSavers.gettingTheBestInvestmentFunds(base_final)
        generalCharts.createChart([10, 6], nomes_fundos, cinco_maiores_valores, valores_cota, cnpjs_fundos)
        _=1

        #s3 = client.createClient('s3')
        #localfile = f"{name_directory}/{fileName}.{file_type}"
        #client.uploadFile(s3, localfile, 'engdadostest', localfile)
        
    except FileNotFoundError as err:
        logging.error(f"ERRO: {generalTools.upperCase(err)}, O ARQUIVO JSON (data.json) NÃO FOI ENCONTRADO.")
    except (rq.exceptions.HTTPError, rq.exceptions.RequestException) as err:
        logging.error(f"ERRO DURANTE A REQUISIÇÃO: {generalTools.upperCase(err)}")
    except Exception as err:
        logging.error(f"ERRO DESCONHECIDO: {generalTools.upperCase(err)}")

if __name__ == '__main__':
    main()