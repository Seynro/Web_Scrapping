from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from bs4 import BeautifulSoup
import time 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Timer start
start = time.time()

def price_taker():
    # Reading downloaded html
    with open(r'C:\Users\user\Desktop\Internship\Web_Scrapping\page.html', 'r', encoding='utf-8') as file:
        html_content = file.read()

    # Creating object BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find element with class "section-title_name" and that contains "ОБЪЯВЛЕНИЯ"
    section_title = soup.find('p', class_='section-title_name', text='ОБЪЯВЛЕНИЯ')

    # Find all next element of class "products-i"
    ads_elements = section_title.find_all_next('div', class_='products-i')
    prices = []

    # combine all prices of one page in one list
    for ad in ads_elements:
        price_tag = ad.find('div', class_='product-price')
        if price_tag:
            price = price_tag.text.strip()
            prices.append(price)

    return prices

df = pd.DataFrame()

# Makes to collect price
makes = ['Audi', 'BMW']

price_from_val = '10000'
price_to_val = '15000'
year_from_val = '2000'
year_to_val = '2015'


# Web-driver (Chrome)
from selenium import webdriver

# Path to Add-on (ad-block)
path_to_adblockplus = r"C:\Users\user\Desktop\Internship\Web_Scrapping\extension_3_18_1_0.crx"

# Settings for Chrome
chrome_options = webdriver.ChromeOptions()
chrome_options.add_extension(path_to_adblockplus)

# Turning on Chrome with add-on
driver = webdriver.Chrome(options=chrome_options)

# Opening main page
driver.get("https://ru.turbo.az/")


for i in makes:
    total = []
#-----------------------------------------------------------------------------------------------

    # Clicking on the dropddown of Makes
    dropdown = driver.find_element(By.CLASS_NAME, "tz-dropdown")
    dropdown.click()

    # Choosing make
    choose_make = driver.find_element(By.XPATH, f"//span[text()='{i}']")
    choose_make.click()

#-----------------------------------------------------------------------------------------------
    # Clicking on the Price from input
    price_from = driver.find_element(By.ID, "q_price_from")

    # Получить текущее значение элемента ввода
    current_value = price_from.get_attribute('value')

    # Проверить, есть ли значение в элементе ввода
    if current_value:
        print("Элемент ввода содержит значение:", current_value)
    else:
        print("Элемент ввода пуст.")
        price_from.send_keys(price_from_val)

#-----------------------------------------------------------------------------------------------
    # Clicking on the Price to input
    price_to = driver.find_element(By.ID, "q_price_to")

    # Получить текущее значение элемента ввода
    current_value = price_to.get_attribute('value')

    # Проверить, есть ли значение в элементе ввода
    if current_value:
        print("Элемент ввода содержит значение:", current_value)
    else:
        print("Элемент ввода пуст.")
        price_to.send_keys(price_to_val)

#-----------------------------------------------------------------------------------------------
    # # Clicking on the dropddown of Year From
    # year_from = (By.CSS_SELECTOR, 'div[data-id="q_year_from"]')
    # wait = WebDriverWait(driver, 3)
    # element = wait.until(EC.element_to_be_clickable(year_from))
    # element.click()

    # # Choosing Year from
    # choose_make = driver.find_element(By.XPATH, f"//span[text()='{year_from_val}']")
    # choose_make.click()

# #-----------------------------------------------------------------------------------------------
#     from selenium.webdriver import ActionChains
#     # Clicking on the dropddown of Year To
#     year_to = (By.CSS_SELECTOR, 'div[data-id="q_year_to"]')
#     wait = WebDriverWait(driver, 3)
#     element = wait.until(EC.element_to_be_clickable(year_to))
#     element.click()

#     # Choosing Year to
#     # Finding Year to
#     choose_year_to = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, f"//span[text()='{year_to_val}']")))

#     # Create ActionChains object
#     actions = ActionChains(driver)

#     # Move to the element and click on it
#     actions.move_to_element(choose_year_to).click().perform()
#-----------------------------------------------------------------------------------------------
    # Click on butten 'Показать результаты'
    show_results = driver.find_element(By.XPATH, f'//*[@id="new_q"]/div/div[4]/div[2]/button')
    show_results.click()

#-----------------------------------------------------------------------------------------------
    pages = 0
    while True:
        pages += 1
        # Save HTML of the current page
        page_html = driver.page_source

        with open('page.html', 'w', encoding='utf-8') as file:
            file.write(page_html)
        
        # Add the list of prices of one page to the global list of one make
        total.extend(price_taker())

        try:
            # Serch for reference on the next page
            next_link = driver.find_element(By.CSS_SELECTOR, 'a[rel="next"]')
            
            # If reference is found then continue
            # Else stop and enter next make
            next_link.click()
            print('PAGE DONE, GOING TO THE NEXT')
            print(pages)
        except:
            print('BREAK')
            print(pages)
            break

    # Creating final df   
    print('MAKE DONE')
    temp_df = pd.DataFrame({i: total})
    df = pd.concat([df, temp_df], axis=1)
    print(df)

driver.quit()

# Convering currencies
def convert_currency(value):
    value_str = str(value)
    if '$' in value_str:
        return float(value_str.replace('$', '').replace(' ', '')) * 1.7
    elif '€' in value_str:
        return float(value_str.replace('€', '').replace(' ', '')) * 1.82
    elif 'AZN' in value_str:
        return float(value_str.replace('AZN', '').replace(' ', ''))
    else:
        return float(value_str.replace(' ', ''))

for col in df.columns:
    df[col] = df[col].apply(convert_currency)

# Exporting as XLSX
df.to_excel('Makes.xlsx')
print(df)

# Time of script work
end = time.time() - start
print(end)