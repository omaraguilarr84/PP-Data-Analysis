from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
import os
import time
import pandas as pd

league = input("What league would you like PP data from? ")

############################################################################

driver = uc.Chrome()

###########################################################################

driver.get("https://app.prizepicks.com/")
time.sleep(3)

WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "close")))
time.sleep(3)
driver.find_element(By.XPATH, "/html/body/div[3]/div[3]/div/div/div[1]").click()
time.sleep(3)

ppPlayers = []

# CHANGE MLB TO ANY SPORT THAT YOU LIKE!!!!! IF THE SPORT IS NOT OFFERED ON PP THEN THE PROGRAM WILL RUN AN ERROR AND EXIT.
driver.find_element(By.XPATH, f"//div[@class='name'][normalize-space()='{league}']").click()
time.sleep(5)

stat_container = WebDriverWait(driver, 1).until(EC.visibility_of_element_located((By.CLASS_NAME, "stat-container")))

categories = driver.find_element(By.CSS_SELECTOR, ".stat-container").text.split('\n')

for category in categories:
    driver.find_element(By.XPATH, f"//div[text()='{category}']").click()

    projectionsPP = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".projection")))

    for projections in projectionsPP:
        names = projections.find_element(By.CLASS_NAME, "name").text
        team_position = projections.find_element(By.CLASS_NAME, "team-position").get_attribute('innerHTML')
        parts = team_position.split('-', 1)
        position = parts[-1].strip()
        opp = projections.find_element(By.CLASS_NAME, "opponent").get_attribute('innerHTML')
        opp = opp[-3:]
        opp = opp.replace(" ",'')
        value = projections.find_element(By.CLASS_NAME, "presale-score").get_attribute('innerHTML')
        proptype = projections.find_element(By.CLASS_NAME, "text").get_attribute('innerHTML')

        # Add demons and goblins for special
        players = {
            'Name': names,
            'Position': position,
            'Opposing Team': opp,
            'Threshold': value,
            'Type': proptype.replace("<wbr>", ""),
            'Special': []
        }
        ppPlayers.append(players)

dfProps = pd.DataFrame(ppPlayers)

file_name = f'{league}_ppData.csv'
file_path = '/Users/omaraguilarjr/PP-Data-Analysis/Data'
full_path = f'{file_path}/{file_name}'

dfProps.to_csv(full_path, index=False)

print("These are all of the props offered by PP.", '\n')
print(dfProps)
print('\n')
