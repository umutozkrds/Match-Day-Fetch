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

def find_matches_for_teams(teams):

    options = Options()
    options.add_argument("--headless")  # Arka planda çalıştırmak için (isteğe bağlı)
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    # Selenium ile tarayıcıyı başlat
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get("https://www.sofascore.com/tr/")

    matches = driver.find_elements(By.XPATH, '//div[contains(@class, "jtsXPN")]')

    found_matches = []
    for match in matches:
        try:
            left_team = match.find_element(By.XPATH, './/div[@data-testid="left_team"]//bdi').text
            right_team = match.find_element(By.XPATH, './/div[@data-testid="right_team"]//bdi').text

            if left_team in teams or right_team in teams:
                found_matches.append(f"{left_team} - {right_team}")
        except NoSuchElementException:
            continue  # Eğer bir takım bulunamazsa devam et
    
    driver.quit()  # Tarayıcıyı kapat
    
    return found_matches

#8196236979:AAHv0bCn9LH3PGa5LF8rmE7rb8MXqv4rsMU