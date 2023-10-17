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
        self.df = pd.DataFrame(columns=['Situacao', 'Var_Desconto', 'Descricao', 'Codigo', 'Avaliacao', 'Preco_Original', 'Preco_A_Vista', 'Produto', 'Desmembrar', 'Desconsiderar'])
        self.resume = {
                    1: self.saveValuesSizeOne, 2: self.saveValuesSizeTwo,
                    3: self.saveValuesSizeThree, 4: self.saveValuesSizeFour,
                    5: self.saveValuesSizeFive, 6: self.saveValuesSizeSix,
                    7: self.saveValuesSizeSeven, 8: self.saveValuesSizeEight,
                    9: self.saveValuesSizeNine, 10: self.saveValuesSizeTen,
                    11: self.saveValuesSizeEleven, 12: self.saveValuesSizeTwelve,
                    13: self.saveValuesSizeThirteen,
                    14: self.saveValuesSizeFourteen, 
                    15: self.saveValuesSizeFifteen, 16: self.saveValuesSizeSixteen
        }

    def saveValuesSizeOne(self, data: list, product: str):
        pass

    def saveValuesSizeTwo(self, data: list, product: str):
        pass

    def saveValuesSizeThree(self, data: list, product: str):
        pass

    def saveValuesSizeFour(self, data: list, product: str):
        if len(data) != 4:
            self.resume.get(len(data), lambda data, product: None)(data, product)
            return
        self.df = pd.concat([self.df, pd.DataFrame([data], columns=['Descricao', 'Codigo', 'Preco_Original', 'Produto'])], ignore_index=True)
    
    def saveValuesSizeFive(self, data: list, product: str):
        if len(data) != 5:
            self.resume.get(len(data), lambda data, product: None)(data, product)
            return
        if "(" in data[2]:
            self.df =  pd.concat([self.df, pd.DataFrame([data], columns=['Descricao', 'Codigo', 'Avaliacao','Preco_Original', 'Produto'])], ignore_index=True)
        else:
            self.df = pd.concat([self.df, pd.DataFrame([data], columns=['Descricao', 'Codigo', 'Preco_Original', 'Desmembrar', 'Produto'])], ignore_index=True)
    
    def saveValuesSizeSix(self, data: list, product: str):
        if len(data) != 6:
            self.resume.get(len(data), lambda data, product: None)(data, product)
            return
        if "(" in data[2]:
            self.df = pd.concat([self.df, pd.DataFrame([data], columns=['Descricao', 'Codigo', 'Avaliacao', 'Preco_Original', 'Desmembrar', 'Produto'])], ignore_index=True) 
        elif 'OFERTA' in data[0]:
            self.df = pd.concat([self.df, pd.DataFrame([data], columns=['Situacao', 'Var_Desconto', 'Descricao', 'Codigo', 'Preco_Original', 'Produto'])], ignore_index=True)
        elif 'à' in data[0] or 's/juro' in data[0]:
            if 'EXCLUSIVO' in data[1]:
                data = ("\n").join(data).split("EXCLUSIVO SITE\n")[-1].split("\n")
                self.resume.get(len(item), lambda item, product: None)(data, product)
                return
            else:
                data = ("\n").join(data).split("s\n")
                for item in data:
                    self.resume.get(len(item), lambda item, product: None)(data, product)
                    return
        elif 'NOVIDADE' in data[0]:
            self.df = pd.concat([self.df, pd.DataFrame([data], columns=['Situacao', 'Descricao', 'Codigo', 'Avaliacao', 'Preco_Original', 'Produto'])], ignore_index=True)
        else:
            print()
    
    def saveValuesSizeSeven(self, data: list, product: str):
        data = transformData.cleaningEmptySpace("\n".join(data).split("EXCLUSIVO SITE")[-1].split("\n"), product)
        data = transformData.cleaningDataRepeated(data)
        if len(data) != 7:
            self.resume.get(len(data), lambda data, product: None)(data, product)
            return 
        if 'Cód' in data[3]:
            self.df = pd.concat([self.df, pd.DataFrame([data], columns=['Situacao', 'Var_Desconto', 'Descricao', 'Codigo', 'Preco_Original', 'Preco_A_Vista', 'Produto'])], ignore_index=True)
        else:
            data = ("\n").join(data).split("cada\n")
            for item in data[:-1]:
                item = item.split("\n")
                item = transformData.cleaningEmptySpace(item, product) if len(item) != 1 else item
                if len(item) != 7:
                    self.resume.get(len(item), lambda item, product: None)(item, product)
            return
    
    def saveValuesSizeEight(self, data: list, product: str):
        if len(data) != 8:
            self.resume.get(len(data), lambda data, product: None)(data, product)
            return
        if 'Cód' in data[3]:
            self.df = pd.concat([self.df, pd.DataFrame([data], columns=['Situacao', 'Var_Desconto', 'Descricao', 'Codigo', 'Preco_Original', 'Preco_A_Vista', 'Desmembrar', 'Produto'])], ignore_index=True) 
        else:
            data = ("\n").join(data).split("cada\n")
            for item in data[:-1]:
                item = item.split("\n")
                item = transformData.cleaningEmptySpace(item, product) if len(item) != 1 else item
                if len(item) != 8:
                    self.resume.get(len(item), lambda item, product: None)(item, product)
            return
    
    def saveValuesSizeNine(self, data: list, product: str):
        if len(data) != 9:
            self.resume.get(len(data), lambda data, product: None)(data, product)
            return
        if '$' in data[4]:
            self.df = pd.concat([self.df, pd.DataFrame([data], columns=['Situacao', 'Var_Desconto', 'Descricao', 'Codigo', 'Preco_Original', 'Preco_A_Vista', 'Desconsiderar', 'Desmembrar', 'Produto'])], ignore_index=True)
        elif "(" in data[4]:
            self.df = pd.concat([self.df, pd.DataFrame([data], columns=['Situacao', 'Var_Desconto', 'Descricao', 'Codigo', 'Avaliacao', 'Preco_Original', 'Preco_A_Vista', 'Desmembrar', 'Produto'])], ignore_index=True)
        else:
            print()

    def saveValuesSizeTen(self, data: list, product: str):
        if len(data) != 10:
            self.resume.get(len(data), lambda data, product: None)(data, product)
            return
        
        if 'Cód.' in data[3]:
            self.df = pd.concat([self.df, pd.DataFrame([data], columns=['Situacao', 'Var_Desconto', 'Descricao', 'Codigo', 'Avaliacao', 'Preco_Original', 'Preco_A_Vista', 'Desconsiderar','Desmembrar', 'Produto'])], ignore_index=True)
        else:
            data = ("\n").join(data).split("cada\n")
            for item in data[:-1]:
                item = item.split("\n")
                item = transformData.cleaningEmptySpace(item, product) if len(item) != 1 else item
                if len(item) != 10 or 's/juro' in item[0]:
                    self.resume.get(len(item), lambda item, product: None)(item, product)
            return
    
    def saveValuesSizeEleven(self, data: list, product: str):
        pass

    def saveValuesSizeTwelve(self, data: list, product: str):
        pass

    def saveValuesSizeThirteen(self, data: list, product: str):
        pass

    def saveValuesSizeFourteen(self, data: list, product: str):
        pass

    def saveValuesSizeFifteen(self, data: list, product: str):
        pass

    def saveValuesSizeSixteen(self, data: list, product: str):
        pass

    def openingSheets(self, directory: str, sheet: str, rows: int, footer: int):
        return pd.read_excel(f"{directory}", sheet_name=f"{sheet}", skiprows=rows, skipfooter=footer)

    def validatingStructure(self, data: str, sep):
        aux_df = pd.DataFrame() # ARQUIVO QUE MANIPULAREI
        novo_df = pd.DataFrame() # O FINAL
        alt_df = pd.DataFrame() # VOU ARMAZENAR AS COLUNAS QUE PRECISAM SER AJUSTADAS
        self.df = pd.read_csv("30k.csv", sep='\t') # ARQUIVO BASE, A SEGURANÇA
        self.df.fillna("", inplace=True)
        aux_df = self.df
        # AJUSTANDO DOCUMENTO BASE

        # COLUNA SITUACAO
        aux_df['Situacao'] = aux_df['Situacao'].map(lambda x: "EXCLUSIVO SITE" if x == '' else x)
        novo_df = aux_df[aux_df['Situacao'].isin(['OFERTA', 'EXCLUSIVO SITE'])]
        alt_df = aux_df[~aux_df['Situacao'].isin(['OFERTA', 'EXCLUSIVO SITE'])]

        # COLUNA VAR_DESCONTO
        tratar = novo_df[novo_df['Var_Desconto'].map(lambda x: '%' in x) == False]
        novo_df = novo_df[novo_df['Var_Desconto'].map(lambda x: '%' in x) == True]
        alt_df = pd.concat([alt_df, tratar])

        # COLUNA DESCRICAO
        tratar = novo_df[novo_df['Descricao'].isin(['OFERTA', 'EXCLUSIVO SITE', 'NOVIDADE'])]
        novo_df = novo_df[~novo_df['Descricao'].isin(['OFERTA', 'EXCLUSIVO SITE', 'NOVIDADE'])]
        alt_df = pd.concat([alt_df, tratar])

        # COLUNA CODIGO
        tratar = novo_df[novo_df['Codigo'].str.contains(r'Cód\. \d+', regex=True) != True]
        novo_df = novo_df[novo_df['Codigo'].str.contains(r'Cód\. \d+', regex=True) == True]
        alt_df = pd.concat([alt_df, tratar])

        # COLUNA AVALIACAO
        tratar = novo_df[novo_df['Avaliacao'].str.contains(r'\(\d+\)|^$', regex=True) != True]
        novo_df = novo_df[novo_df['Avaliacao'].str.contains(r'\(\d+\)|^$', regex=True) == True]
        alt_df = pd.concat([alt_df, tratar])
        
        # COLUNA PRECO_ORIGINAL
        tratar = novo_df[novo_df['Preco_Original'].str.contains(r'R\$\s?(\d{1,3}(?:\.\d{3})*(?:,\d{2})?)\s?cada', regex=True) != True]
        novo_df = novo_df[novo_df['Preco_Original'].str.contains(r'R\$\s?(\d{1,3}(?:\.\d{3})*(?:,\d{2})?)\s?cada', regex=True) == True]
        alt_df = pd.concat([alt_df, tratar])

        # COLUNA PRECO_A_VISTA
        tratar = novo_df[novo_df['Preco_A_Vista'].str.contains(r'R\$\s?(\d{1,3}(?:\.\d{3})*(?:,\d{2})?)\s?cada', regex=True) != True]
        novo_df = novo_df[novo_df['Preco_A_Vista'].str.contains(r'R\$\s?(\d{1,3}(?:\.\d{3})*(?:,\d{2})?)\s?cada', regex=True) == True]
        alt_df = pd.concat([alt_df, tratar])
        
        # COLUNA PRODUTO

        # COLUNA DESMEMBRAR
        tratar = novo_df[novo_df['Desmembrar'].str.contains('R\$\s?\d{1,3}(?:\.\d{3})*(?:,\d{2})?(?:\s?(?:em até|de)?\s?\d{1,2}x\s?de\s?R\$\s?\d{1,3}(?:\.\d{3})*(?:,\d{2})?\s?(?:s/juros)?)?|^$', regex=True) != True]
        novo_df = novo_df[novo_df['Desmembrar'].str.contains('R\$\s?\d{1,3}(?:\.\d{3})*(?:,\d{2})?(?:\s?(?:em até|de)?\s?\d{1,2}x\s?de\s?R\$\s?\d{1,3}(?:\.\d{3})*(?:,\d{2})?\s?(?:s/juros)?)?|^$', regex=True) == True]
        alt_df = pd.concat([alt_df, tratar])

        # COLUNA DESCONSIDERAR
        tratar = novo_df[novo_df['Desconsiderar'].str.contains('à vista no pix|^$', regex=True) != True]
        novo_df = novo_df[novo_df['Desconsiderar'].str.contains('à vista no pix|^$', regex=True) == True]
        alt_df = pd.concat([alt_df, tratar])
        
        novo_df['Data_Captura'] = generalTools.splitByEmptySpace(data)[0]

        return novo_df, alt_df

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

    def identifyTheWorstProducts(self, df: pd.DataFrame, num_faixas: int):
        df = df[df['Avaliacao'].map(lambda x: 0 if x == '' else int(x)) > 0]
        df.reset_index(inplace=True)
        df.drop('index', axis=1, inplace=True)
        df['Metrica_Ruim'] = 1 / df['Avaliacao'].astype(int)

        # Divide os dados da coluna Preco Original em faixas (bins)
        df['Faixa_de_Preco'] = pd.cut(df['Preco_Original'].map(lambda x: float(x)), bins=num_faixas)

        # Agrupando os dados por produto e faixa de preço, e encontra a média da métrica ruim 
        grupo = df.groupby(['Produto', 'Faixa_de_Preco'])['Metrica_Ruim'].mean().reset_index()

        # Encontra os piores produtos por produto e faixa de preço
        piores_produtos = grupo.groupby('Produto').apply(lambda x: x.nsmallest(1, 'Metrica_Ruim')).reset_index(drop=True)

        grupo['Faixa_de_Preco_Mid'] = grupo['Faixa_de_Preco'].apply(lambda x: x.mid)

        # Plotando o gráfico (experimento)
        generalCharts.createChart([12, 8], piores_produtos, grupo)