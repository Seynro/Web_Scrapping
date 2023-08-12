from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

import time
import main

make = 'Audi'
# Запустите веб-драйвер (например, Chrome)
driver = webdriver.Chrome()

# Откройте главную страницу
driver.get("https://ru.turbo.az/")

# нажимаем Дропдаун
dropdown = driver.find_element(By.CLASS_NAME, "tz-dropdown")
dropdown.click()

# Выбираем модель
choose_make = driver.find_element(By.XPATH, f"//span[text()='{make}']")
choose_make.click()
time.sleep(1)

show_results = driver.find_element(By.XPATH, f'//*[@id="new_q"]/div/div[4]/div[2]/button')
show_results.click()

time.sleep(1)

# Сохраните HTML текущей страницы
page_html = driver.page_source

with open('page.html', 'w', encoding='utf-8') as file:
    file.write(page_html)

driver.quit()

main.price_taker()



