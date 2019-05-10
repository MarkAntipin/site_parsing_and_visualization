from bs4 import BeautifulSoup
import requests
import re

import asyncio
import aiohttp

import pandas as pd


def parse_catalog(main_link, previous_link, catalog_links):
    page = requests.get(main_link)
    soup = BeautifulSoup(page.content, 'html.parser')
    tags = soup.find_all('a',href=True)
    main_link = main_link.replace(previous_link, '')
    for tag in tags:
        link = tag['href']
        if re.search(r'\/pages', str(link)) and link not in catalog_links:
            if re.search(r'javascript',str(link)):
                break
            catalog_links.add(link)
            previous_link = link
            parse_catalog(main_link+str(link), previous_link, catalog_links)


def parse_product(main_link, product_links):
    page = requests.get(main_link)
    soup = BeautifulSoup(page.content, 'html.parser')
    tags = soup.find_all('a', href=True)
    for tag in tags:
        link = tag['href']
        if re.search(r'\/product', str(link)):
            if re.search(r'javascript',str(link)) is None:
                product_links.add(link)


def save_links_to_file(main_link, file_path):
    '''
    парсинг по всем каталогам сайта
    и добавление ссылок на товары в файл
    "hatewait.txt"
    '''
    product_links = set()
    final_catalogs = set()
    parse_catalog(main_link, '', final_catalogs)

    for catalog in final_catalogs:
        parse_product(main_link + catalog, product_links)

    fl = open(file_path, 'w+')
    for i in product_links:
        fl.write(main_link + str(i) + '\n')
    fl.close()


def parse_page(page_link):
    '''
    парсинг страницы
    :param ссылка на страницу продукта:
    :return значения name, price, brand, category для товара:
    '''
    try:
        page = requests.get(page_link)
        soup = BeautifulSoup(page.content, 'html.parser')
        name = soup.find('h1').text
        temp = name.split(' ')
        brand = temp[1]
        price = int(re.findall(r"\d+\s\d+", str(soup.find("h2")))[0].replace('\xa0', ''))

        category = soup.find("span", attrs={"class": ['n-product-spec__value-inner']}).text

        return name, price, brand, category
    except:
        return None, None, None, None


def get_country_from_brand(brand):
    '''
    добавить атрибут 'country'
    к нашему датафрейму
    '''
    country_to_brand = {'China': ['Huawei', 'Xiaomi', 'OnePlus'],
                        'USA': ['Apple', 'Beats', 'GarmiH', 'Google'],
                        'South Korea': ['Samsung', 'LG'],
                       'Japan': ['Sony']}
    for i in country_to_brand.keys():
        if brand in country_to_brand[i]:
            return i
    return None


def make_dataframe(product_links_file):
    '''
    формирование датафрейма
    сайт кривой и я кривой поэтому вот так)
    :param путь до файла где лежат ссылки на товары:
    :return датафрейм с атрибутами 'name', 'price', 'brand',
                                  'category', 'url', 'country'}:
    '''
    name = []
    price = []
    brand = []
    category = []
    # url = []
    countries = []
    with open(product_links_file) as file:
        for link in file:
            # url.append(link)
            a = parse_page(link[:-1])
            if None in a:
                continue
            name.append(a[0])
            price.append(a[1])

            temp_brand = a[2]
            if 'Беспроводные' in a[2] or 'Смарт' in a[2]:
                temp = a[0].split(' ')
                temp_brand = temp[3]
            if 'Браслет' in a[2] or 'Наушники' in a[2] or 'Смартфон' in a[2]:
                temp = a[0].split(' ')
                temp_brand = temp[2]
            if 'Ноутбук' in a[2] or 'Фитнес-браслет' in a[2] or 'Redmi' in a[2]:
                temp_brand = 'Xiaomi'
            if 'Смарт' in a[2] or 'Samsung' in a[2]:
                temp_brand = 'Samsung'
            if 'Xperia' in a[2]:
                temp_brand = 'Sony'
            if 'Garmih' in a[2]:
                temp_brand = 'GarmiH'
            brand.append(temp_brand)

            country = get_country_from_brand(temp_brand)
            countries.append(country)

            temp_category = a[3]
            if '1920x1080' in a[3]:
                temp_category ='ноутбук'
            if 'Bluetooth' in a[3]:
                temp_category = 'Bluetooth-наушники с микрофоном'
            if 'смартфон' in a[3]:
                temp_category = 'смартфон'
            category.append(temp_category)

    site_data = pd.DataFrame({'name': name, 'price': price, 'brand': brand,
                              'country': countries, 'category': category}).dropna()
    site_data.to_csv('site_data.csv', encoding='utf-8')
    return site_data
