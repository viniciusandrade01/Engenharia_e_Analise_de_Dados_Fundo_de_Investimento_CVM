import requests as rq
import os
import zipfile
import utils.logger_config as logger_config
import logging
import locale
from utils.tools import GeneralTools

generalTools = GeneralTools()
jsonData = generalTools.openJson()
locale.setlocale(locale.LC_ALL, 'pt_BR.utf8')
logger_config.setup_logger(generalTools.getDate())

class DriverChrome:
    def __init__(self):
        # URL para verificar a versão mais recente do Chrome
        self.chrome_version_url = 'https://chromedriver.storage.googleapis.com/LATEST_RELEASE'

        # URL base para baixar o ChromeDriver
        self.chrome_driver_base_url = 'https://chromedriver.storage.googleapis.com/'

    def getLatestChromeVersion(self):
        response = rq.get(self.chrome_version_url)
        if response.status_code == 200:
            return response.text.strip()
        else:
            raise Exception("Não foi possível obter a versão mais recente do Chrome.")

    def downloadChromeDriver(self, version, destination_directory):
        chrome_driver_url = f"{self.chrome_driver_base_url}{version}/chromedriver_win32.zip"
        
        response = rq.get(chrome_driver_url)
        if response.status_code == 200:
            zip_file_path = os.path.join(destination_directory, 'chromedriver_win32.zip')
            
            with open(zip_file_path, 'wb') as file:
                file.write(response.content)
            
            with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                zip_ref.extractall(destination_directory)
            
            os.remove(zip_file_path)
        else:
            raise Exception(f"Não foi possível baixar o ChromeDriver versão {version}.")