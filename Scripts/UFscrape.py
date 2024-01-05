from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import undetected_chromedriver as uc
import os
import time
import pandas as pd

league = input("What league would you like PP data from? ")

############################################################################

driver = uc.Chrome()

###########################################################################

url = f"https://underdogfantasy.com/pick-em/higher-lower/all/"
email = 'omar.hawks8@gmail.com'
password = 'Jun20jun02!'

driver.get(url)
time.sleep(5)

email_input = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[2]/div[2]/div[1]/form/div[1]/label/div[2]/input')
password_input = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[2]/div[2]/div[1]/form/div[2]/label/div[2]/input')
submit_button = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[2]/div[2]/div[1]/form/button')

email_input.send_keys(email)
password_input.send_keys(password)
submit_button.click()
time.sleep(10)

driver.find_element(By.XPATH, f'//p[text()="{league}"]').click()
time.sleep(3)

ufPlayers = []

games = driver.find_elements(By.CSS_SELECTOR, '[data-testid="accordion"]')

for game in games:
    players = game.find_elements(By.CSS_SELECTOR, '[data-testid="over-under-cell"]')

    for player in players:
        try:
            player.find_element(By.CLASS_NAME, 'styles__toggleButton__jrfS7').click()
        except NoSuchElementException:
            pass

        name = player.find_element(By.CSS_SELECTOR, '[data-testid="player-name"]').text
        loc_opp = player.find_element(By.CLASS_NAME, "styles__matchInfoText__klQeu").get_attribute('innerHTML').split(' ')
        opp = loc_opp[2]

        props = player.find_elements(By.CSS_SELECTOR, '[data-testid="over-under-list-cell"]')

        for prop in props:
            idk = prop.find_element(By.CSS_SELECTOR, '[data-testid="stat-line"]')
            line_prop = idk.find_element(By.XPATH, './/div/div/p').get_attribute('innerHTML')
            line_prop = line_prop.split(' ', 1)
            line = line_prop[0]
            propType = line_prop[1].replace(' ','')

            options = prop.find_elements(By.CSS_SELECTOR, '[data-testid="option-button"]')
            if len(options) == 2:
                special = ''
            else:
                h_l = prop.find_element(By.CLASS_NAME, 'styles__optionText__zDwBZ').text
                mult = prop.find_element(By.CLASS_NAME, 'styles__payoutMultiplier__RBcHU').text
                special = f'{h_l} {mult}'

            x = {
                'Name': name,
                'Position': [],
                'Opposing Team': opp,
                'Threshold': line,
                'Type': propType,
                'Special': special
            }
            ufPlayers.append(x)

dfProps = pd.DataFrame(ufPlayers)

file_name = f'{league}_ufData.csv'
file_path = '/Users/omaraguilarjr/PP-Data-Analysis/Data'
full_path = f'{file_path}/{file_name}'

dfProps.to_csv(full_path, index=False)

print("These are all of the props offered by UF.", '\n')
print(dfProps)
print('\n')
            