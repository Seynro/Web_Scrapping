from bs4 import BeautifulSoup


def price_taker():
    # Чтение файла
    with open(r'C:\Users\user\Desktop\Internship\Web_Scrapping\page.html', 'r', encoding='utf-8') as file:
        html_content = file.read()

    # Создание объекта BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Находим все элементы объявлений с классом "products-i" и извлекаем цены
    ads_elements = soup.find_all('div', class_='products-i')
    prices = []

    for ad in ads_elements:
        price_tag = ad.find('div', class_='product-price')
        if price_tag:
            price = price_tag.text.strip()
            prices.append(price)

    print(prices)


