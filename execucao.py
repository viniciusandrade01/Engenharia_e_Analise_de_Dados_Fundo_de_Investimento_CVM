import pandas as pd
import requests as rq
from methods.loaders.filesSave import FileSavers
from methods.transformers.transformData import TransformData
from methods.extractors.webPageDataScrapers import WebPageDataScrapers
from utils.tools import GeneralTools
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
        df = pd.DataFrame()
        client = AboutAWS()
        # Variável contendo informações das moedas a serem coletadas, aws e banco de dados
        jsonData = generalTools.openJson()
        logger_config.setup_logger(generalTools.getDate())
        
        # CONFIGURANDO PARA 4 CASAS DECIMAIS A FORMATAÇÃO E EXIBIÇÃO DOS N°S DE PONTO FLUTUANTE 
        pd.options.display.float_format = '{:.4f}'.format

        name_directory = f"{jsonData['source']['generalLink']['params']['directory']}{generalTools.hyphenToNull(generalTools.splitByEmptySpace(generalTools.getDate())[0])}"
        nameFile = transformData.getFileName(jsonData)
        dataRef = nameFile.split("_")[-1].split(".")[0] if isinstance(nameFile, str) else 'HISTÓRICA'
        nameFile = iter([nameFile]) if isinstance(nameFile, str) else iter(nameFile)
        generalTools.makeDirectory(name_directory)
        dados_fundos = []

        for file in nameFile:
            html, soup = webPageDataScrapers.requestGetDefault(f"{jsonData['source']['generalLink']['url']}{file}")
            webPageDataScrapers.downloadUrl(html, file, name_directory)
            logging.info("INFORMAÇÕES DA URL BAIXADA COM SUCESSO.")
            zip_file = webPageDataScrapers.readZipFile(file, name_directory)
            dados_fundos.append(fileSavers.readDeepData(zip_file))

        #dados_fundos = fileSavers.readDeepData(zip_file)
        dados_cadastro = fileSavers.readRegistrationData()
        dados_fundos_filtrado = transformData.gettingMonthlyReturn(dados_fundos)
        base_final = fileSavers.mergeDataFrames(dados_fundos_filtrado, dados_cadastro)
        maiores_valores, nomes_fundos, valores_cota, cnpjs_fundos = fileSavers.gettingTheBestInvestmentFunds(base_final, jsonData['source']['generalLink']['params']['toprange'])
        base_final = transformData.ajustingColumns(base_final)
        generalCharts.createBarhChart([10, 6], nomes_fundos, cnpjs_fundos, maiores_valores, dataRef, name_directory, jsonData['source']['generalLink']['params']['toprange'])
        #generalCharts.createChart([10, 6], nomes_fundos, maiores_valores, valores_cota, cnpjs_fundos)
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