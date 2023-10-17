from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class GeneralSelenium:
    def __init__(self):
        pass

    def startSelenium(self):
        return webdriver.Chrome()

    def navegateUrl(self, driver, url):
        return driver.get(url)

    def getTitle(self, driver):
        return driver.title

    def waiting(self, driver, time: int):
        driver.implicitly_wait(time)

    def ClosingSelenium(self):
        return webdriver.Chrome()
    
    def clickOnElementByXPath(self, driver, xpath, time: int):
        try:
            elemento = WebDriverWait(driver, time).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            elemento.click()
        except Exception as e:
            print(f"Erro ao clicar no elemento com XPath: {xpath}")
            print(str(e))