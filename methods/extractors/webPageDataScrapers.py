#import boto3
import zipfile
import os
import requests as rq
from bs4 import BeautifulSoup as bs4
import utils.logger_config as logger_config
import logging
import locale
from utils.tools import GeneralTools
from utils.aws import AboutAWS

generalTools = GeneralTools()
jsonData = generalTools.openJson()
locale.setlocale(locale.LC_ALL, 'pt_BR.utf8')
logger_config.setup_logger(generalTools.getDate())

class WebPageDataScrapers:
    def __init__(self):
        self.client = AboutAWS()

    def extractZip(self, nome_zip: str, namedirectory: str):
        generalTools.makeDirectory(namedirectory)
        with zipfile.ZipFile(nome_zip, 'r') as zip_ref:
            zip_ref.extractall(namedirectory)
            zip_ref.close()

        # Remova o arquivo ZIP depois de extraído
        os.remove(nome_zip)

    def downloadUrl(self, response, nome_arquivo, namedirectory):
        #nome_arquivo = f"{namedirectory}/{nome_arquivo.split('?')[0]}{generalTools.increase()}.txt" if '?' in nome_arquivo else f"{namedirectory}/{nome_arquivo}{generalTools.increase()}.txt"
        for file in nome_arquivo:
            with open(f"{namedirectory}/{file}", 'wb') as file:
                file.write(response.content)
                #client = self.client.createClient('s3')
                #self.client.uploadFile(client, nome_arquivo, 'engdadostest', nome_arquivo)

    def requestGetDefault(self, link: str):
        try:
            html = rq.get(link)
            html.raise_for_status()
            soup = bs4(html.text, 'html.parser')

        except rq.exceptions.HTTPError as http_err:
            logging.error(f"Erro HTTP: {http_err}")
        except rq.exceptions.RequestException as req_err:
            logging.error(f"Erro de Requisição: {req_err}")
        except Exception as err:
            logging.error(f"Erro Desconhecido: {err}")
        
        return html, soup