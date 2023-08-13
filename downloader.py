from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from bs4 import BeautifulSoup
import time 

start = time.time()

def price_taker():
    # Чтение файла
    with open(r'C:\Users\user\Desktop\Internship\Web_Scrapping\page.html', 'r', encoding='utf-8') as file:
        html_content = file.read()

    # Создание объекта BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Найдем элемент с классом "section-title_name" и содержимым "ОБЪЯВЛЕНИЯ"
    section_title = soup.find('p', class_='section-title_name', text='ОБЪЯВЛЕНИЯ')

    # Найдем все последующие элементы с классом "products-i"
    ads_elements = section_title.find_all_next('div', class_='products-i')
    prices = []

    for ad in ads_elements:
        price_tag = ad.find('div', class_='product-price')
        if price_tag:
            price = price_tag.text.strip()
            prices.append(price)

    print(prices)

    return prices



df = pd.DataFrame()


makes = ['Audi', 'BMW', 'Toyota', 'Mercedes']
# Запустите веб-драйвер (например, Chrome)
driver = webdriver.Chrome()

# Откройте главную страницу
driver.get("https://ru.turbo.az/")


for i in makes:
    total = []
    # нажимаем Дропдаун
    dropdown = driver.find_element(By.CLASS_NAME, "tz-dropdown")
    dropdown.click()

    # Выбираем модель
    choose_make = driver.find_element(By.XPATH, f"//span[text()='{i}']")
    choose_make.click()

    show_results = driver.find_element(By.XPATH, f'//*[@id="new_q"]/div/div[4]/div[2]/button')
    show_results.click()

    while True:
        # Сохраните HTML текущей страницы
        page_html = driver.page_source

        with open('page.html', 'w', encoding='utf-8') as file:
            file.write(page_html)
        total.extend(price_taker())

        try:
            # Поиск ссылки на следующую страницу
            next_link = driver.find_element(By.CSS_SELECTOR, 'a[rel="next"]')
            
            # Если ссылка найдена, обновляем URL для следующей итерации
            # Иначе завершаем цикл
            next_link.click()
        except:
            break
    
    temp_df = pd.DataFrame({i: total})
    df = pd.concat([df, temp_df], axis=1)
    print(df)

driver.quit()

df.to_excel('Makes.xlsx')
print(df)

end = time.time() - start ## собственно время работы программы

print(end)