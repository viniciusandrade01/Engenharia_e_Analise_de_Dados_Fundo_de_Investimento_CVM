import os
import pandas as pd
import requests as rq
from methods.loaders.filesSave import FileSavers
from methods.transformers.transformData import TransformData
from methods.extractors.webPageDataScrapers import WebPageDataScrapers
from utils.tools import GeneralTools
from utils.driver import DriverChrome
from utils.selenium import GeneralSelenium
import utils.logger_config as logger_config
from utils.aws import AboutAWS
import logging

def main():
    try:
        fileSavers = FileSavers()
        transformData = TransformData()
        webPageDataScrapers = WebPageDataScrapers()
        generalTools = GeneralTools()
        driverChrome = DriverChrome()
        selenium = GeneralSelenium()
        df = pd.DataFrame()
        client = AboutAWS()
        # Variável contendo informações das moedas a serem coletadas, aws e banco de dados
        jsonData = generalTools.openJson()
        logger_config.setup_logger(generalTools.getDate())
        
        name_directory = f"{jsonData['source']['generalLink']['params']['directory']}{generalTools.hyphenToNull(generalTools.splitByEmptySpace(generalTools.getDate())[0])}"

        generalTools.makeDirectory(name_directory)

        html, soup = webPageDataScrapers.requestGetDefault(f"{jsonData['source']['generalLink']['url']}inf_diario_fi_{jsonData['source']['generalLink']['params']['year']}{jsonData['source']['generalLink']['params']['month']}.zip")
        webPageDataScrapers.downloadUrl(html, f"{jsonData['source']['generalLink']['params']['namehtml']}", name_directory)
        logging.info("INFORMAÇÕES DA URL BAIXADA COM SUCESSO.")
        
        

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