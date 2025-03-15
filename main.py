from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time
import pickle
from favori import *

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://www.sofascore.com/tr/")

matches = driver.find_elements(By.XPATH, '//div[contains(@class, "jtsXPN")]')


def find_match(teams):


    found = False  # Maç bulundu mu?
    for match in matches:
        try:
            left_team = match.find_element(By.XPATH, './/div[@data-testid="left_team"]//bdi').text
            right_team = match.find_element(By.XPATH, './/div[@data-testid="right_team"]//bdi').text

            if left_team in teams or right_team in teams:
                print(f"Bugün günlerden {left_team if left_team in teams else right_team} Maç: {left_team} - {right_team}")
                found = True

        except NoSuchElementException:
            continue  # Eğer bir takım bulunamazsa devam et
    
    if not found:
        print("Belirtilen takım(lar) için bugün maç bulunamadı.")

find_match(favorilerim())
driver.close()