import os
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
import seaborn as sns

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
        
        # Configurando para 4 casas decimais a formatação e exibição dos n°s com ponto flutuante
        pd.options.display.float_format = '{:.4f}'.format
        logging.info("CONFIGURAÇÃO PARA 4 CASAS DECIMAIS NOS N°S COM PONTO FLUTUANTE REALIZADA COM SUCESSO.")

        file_name = transformData.getFileName(jsonData)
        directory_name = f"{jsonData['source']['generalLink']['params']['directory']}{file_name.split('_')[-1].split('.')[0]}"
        logging.info("NOME DO DIRETÓRIO COLETADO COM SUCESSO.")
        reference_date = file_name.split("_")[-1].split(".")[0] if isinstance(file_name, str) else 'HISTÓRICA'
        logging.info("DATA REFERÊNCIA COLETADA COM SUCESSO.")
        file_name = iter([file_name]) if isinstance(file_name, str) else iter(file_name)
        generalTools.makeDirectory(directory_name)
        logging.info("NOME DO ARQUIVO COLETADO COM SUCESSO.")
        fund_data = []

        for file in file_name:
            html, soup = webPageDataScrapers.requestGetDefault(f"{jsonData['source']['generalLink']['url']}{file}")
            webPageDataScrapers.downloadUrl(html, file, directory_name)
            logging.info("INFORMAÇÕES DA URL BAIXADA COM SUCESSO.")
            zip_file = webPageDataScrapers.readZipFile(file, directory_name)
            fund_data.append(fileSavers.readDeepData(zip_file))
            logging.info("LEITURA E ARMAZENAMENTO DO CONTEÚDO DO ZIP REALIZADO COM SUCESSO.")

        registration_data = fileSavers.readRegistrationData()
        logging.info("ARMAZENANDO DADOS DE REGISTRO SOBRE OS CNPJS.")
        filtered_fund_data = transformData.gettingMonthlyReturn(fund_data)
        final_base = fileSavers.mergeDataFrames(filtered_fund_data, registration_data)
        logging.info("MESCLANDO OS DADOS ATRAVÉS DA COLUNA CNPJ E ESCOLHE AS COLUNAS DESEJADAS.")
        largest_values, fund_names, quota_values, fund_cnpjs, index, historical_data = fileSavers.gettingTheBestInvestmentFunds(final_base, jsonData['source']['generalLink']['params']['toprange'])
        logging.info(f"ORGANIZANDO DADOS E FILTRANDO OS {jsonData['source']['generalLink']['params']['toprange']} MELHORES FUNDOS.")
        final_base = transformData.ajustingColumns(final_base)

        # Análise dos 'toprange' (inserido no data.json) fundos com maiores Patrimônios Líquidos
        generalCharts.createBarhChart([10, 6], fund_names, fund_cnpjs, largest_values, reference_date, directory_name, jsonData['source']['generalLink']['params']['toprange'])
        logging.info("GRÁFICO DE ANÁLISE DOS 'TOPRANGE' FUNDOS COM MAIORES PATRIMÔNIOS LÍQUIDOS.")

        # Análise da Evolução do Valor Patrimonial Líquido dos 'toprange' ao Longo do Tempo
        generalCharts.netAssetValueEvolution([10, 8], final_base, 'Evolução do Valor Patrimonial Líquido', 'Datas', 'Valores Patrimoniais Líquidos (R$)', 90, reference_date, directory_name, fund_names, fund_cnpjs, largest_values)
        logging.info("GRÁFICO DE ANÁLISE DA EVOLUÇÃO DO VALOR PATRIMONIAL LÍQUIDO DOS 'TOPRANGE' AO LONGO DO TEMPO.")

        # Análise da Distribuição dos Tipos de Fundos ocupados no 'toprange' (TP_FUNDO)
        generalCharts.barChart([10, 8], final_base[final_base['DENOM_SOCIAL'].isin(fund_names)], 'DENOM_SOCIAL', 'TP_FUNDO', 'Distribuição  dos Tipos de Fundos do TopRange', 'Tipo de Fundo', 'Quantidade por Tipo Fundos (Int)', 45, reference_date, directory_name, 'DistribuicaoTiposMelhoresFundos')
        logging.info("GRÁFICO DE ANÁLISE DA DISTRIBUIÇÃO DOS TIPOS DE FUNDOS OCUPADOS NO 'TOPRANGE'.")

        # Análise da Distribuição Geral dos Tipos de Fundos (TP_FUNDO)
        generalCharts.barChart([10, 8], final_base, 'DENOM_SOCIAL', 'TP_FUNDO', 'Distribuição Geral dos Tipos de Fundos', 'Tipo de Fundo', 'Quantidade por Tipo Fundos (Int)', 45, reference_date, directory_name, 'DistribuicaoTiposFundos')
        logging.info("GRÁFICO DE ANÁLISE DA DISTRIBUIÇÃO GERAL DOS TIPOS DE FUNDOS OCUPADOS NO 'TOPRANGE'.")

        fileSavers.dfToCsv(final_base, f'{directory_name}/FundosInvestimentoGeral_{directory_name.split("_")[-1]}.csv', "\t")
        fileSavers.dfToCsv(final_base[final_base['CNPJ_FUNDO'].isin(fund_cnpjs)], f'{directory_name}/FundosInvestimentoTopRange_{directory_name.split("_")[-1]}.csv', "\t")
        
        s3 = client.createClient('s3')
        for arquivos in os.listdir(directory_name):
            localfile = f"{directory_name}/{arquivos}"
            client.uploadFile(s3, localfile, 'engdadostest', localfile)
        logging.info(f"TODOS OS ARQUIVOS (ZIP, CSV E GRÁFICOS) INSERIDOS NA PASTA {directory_name} FORAM INSERIDOS NO BUCKET RESPECTIVO'.")
        
    except FileNotFoundError as err:
        logging.error(f"ERRO: {generalTools.upperCase(err)}, O ARQUIVO JSON (data.json) NÃO FOI ENCONTRADO.")
    except (rq.exceptions.HTTPError, rq.exceptions.RequestException) as err:
        logging.error(f"ERRO DURANTE A REQUISIÇÃO: {generalTools.upperCase(err)}")
    except Exception as err:
        logging.error(f"ERRO DESCONHECIDO: {generalTools.upperCase(err)}")

if __name__ == '__main__':
    main()