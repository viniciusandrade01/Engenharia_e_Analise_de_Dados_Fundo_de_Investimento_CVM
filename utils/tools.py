import json
import os
import datetime
import logging
import re
from unidecode import unidecode
import pandas as pd

class GeneralTools:
    def __init__(self):
        self.contador = 0

    def validateDate(self, data: str, data_param: dict):
        try:
            data_param = f"{data_param['year']}-{data_param['month']}"
            return data if data_param > data[:-3] else f"{data_param}-01"
        except ValueError:
            logging.info ("A ESTRUTURA DA DATA_PARAM NÃO É VÁLIDA. DEVE SER NO FORMATO '%Y-%m', EX.: Year = 2023, Month = 06")
    
    def makeDirectory(self, directory: str):
        if not os.path.exists(directory):
            os.makedirs(directory)

    def getDate(self):
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def openJson(self):
        with open('utils\data.json') as json_file:
            return json.load(json_file)
    
    def hyphenToNull(self, dado: str):
        return dado.replace("-","")
    
    def barToNull(self, dado: str):
        return dado.replace("/"," ")

    def plusToNull(self, dado: str):
        return dado.replace("+","")
    
    def removeEmptySpaceInStr(self, dado: str):
        return dado.lstrip().rstrip()
    
    def hyphenToEmptySpace(self, dado: str):
        return dado.replace("-"," ")
    
    def splitByEmptySpace(self, dado: str):
        return dado.split(" ")
    
    def brlToEmpty(self, dado: str):
        return dado.replace("R$","")
    
    def cleaningAll(self, dado: str):
        return dado.replace("á","a").replace("ã","a").replace("ó","o").replace("ç","c").replace("é","e")
    
    def commaToEmpty(self, dado: str):
        return dado.replace(",","")

    def replaceCommaToDot(self, dado: str):
        return dado.replace(",",".")
    
    def dotToEmpty(self, dado: str):
        return dado.replace(".","")
    
    def emptyValueToEmpty(self, dado: str):
        return dado.replace (" ","")
    
    def percentageToEmpty(self, dado: str):
        return dado.replace("%","")

    def zeroToEmpty(self, dado: str):
        return dado.replace("0","")
    
    def nanToEmpty(self, dado: str):
        return dado.replace("nan", "")
    
    def cleaningStr(self, dado: str):
        return dado.replace('"', "").replace("”", "")
    
    def removeParentheses(self, dado: str):
        return dado.replace("(","").replace(")","")
    
    def removeMinus(self, dado: str):
        return dado.replace("-","")
    
    def removeEllipsis(self, dado: str):
        return dado.replace("...","")
    
    def replaceCommaToDot(self, dado: str):
        return dado.replace(",", ".")
    
    def upperCase(self, dado: str):
        return dado.upper()
    
    def cleaningDataStr(self, data: str):
        return unidecode(data)
    
    def lowerCase(self, dado: str):
        return dado.lower()

    def increase(self):
        self.contador += 1
        return self.contador
    
    def checkValue(self, data):
        return 'CONTINUAR' if len(data) != 0 else 'ENCERRAR'

    def checkValueWithComparation(self, data, page):
        return 'NEXT' if page.split("\n")[0] == data[0] else 'CONTINUAR'
    
    def checkEmptyValue(self, page):
        return 'NEXT' if page == '' else 'CONTINUAR'

    def extractValue(self, text, padrao):
        modelo = padrao
        correspondencia = re.search(modelo, text)
        return correspondencia.group(1) if correspondencia else ""

    def extractNumber(self, texto, padrao):
        match = re.search(padrao, texto)
        if match:
            return match.group(1)
        else:
            return None
    
    def extractTwoValue(self, text, padrao1, padrao2, df):
        correspondencia1 = re.search(padrao1, text)
        correspondencia2 = re.search(padrao2, text)

        if correspondencia1:
            #numero_de_parcelas = correspondencia1.group(1)
            #preco_por_parcela = correspondencia1.group(2)
            #return numero_de_parcelas, preco_por_parcela
            return "%.2f" % float(int(correspondencia1.group(1)) * float(self.replaceCommaToDot(correspondencia1.group(2))))
        elif correspondencia2:
            #preco_total = correspondencia2.group(1)
            #numero_de_parcelas = correspondencia2.group(2)
            #preco_por_parcela = correspondencia2.group(3)
            return "%.2f" % float(int(correspondencia2.group(2)) * float(self.replaceCommaToDot(correspondencia2.group(3))))
        else:
            return ""
        
    def updatePrice(self, row):
        return row['Desmembrar'] if pd.notna(row['Desmembrar']) else row['Preco_Original']

    def updatePriceTypeTwo(self, row):
        return row['Desmembrar'] if pd.notna(row['Desmembrar']) else row['Preco_Original']

    def updateCodeColumn(self, row):
        return int(row) if pd.to_numeric(row) else ""
    
    def checkValueOfTheColumn(self, columnName, type):
        self.df = self.df[pd.to_numeric(self.df[columnName], errors='coerce').notnull()]
        self.df[columnName] = self.df[columnName].astype(int)