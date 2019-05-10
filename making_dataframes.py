'''
разобьем весь датафрейм на сущности:
product(id, name, price, id_brand, id_category, url)
brand(id_brand, name, id_country)
country(id_country, name)
category(id_category, name)

и выложим все на Google BigQuery
'''

import numpy as np
import pandas as pd
from site_parsing import get_country_from_brand


from google.oauth2 import service_account
from google.cloud import bigquery


credentials = service_account.Credentials.from_service_account_file(
    'tokens/grand-cosmos-237507-ec91e6d1934e.json')

private_key = "tokens/grand-cosmos-237507-ec91e6d1934e.json"

project_id = 'grand-cosmos-237507'


def read_data_csv(site_data_csv):
    site_data = pd.read_csv(site_data_csv)
    return site_data


def make_country_data(site_data):
    '''
    также заменяет значения стран в исходном датафрейме
    на индексы
    :param исходный датафрейм:
    :return country(id_country, name) датафрейм
    '''
    unique_countries = np.unique(site_data['country'])
    countries_data = pd.DataFrame({'name': unique_countries})
    # site_data['country'].replace(unique_countries, countries_data.index.to_list(), inplace=True)
    return countries_data


def make_brands_data(site_data, countries_data):
    '''
    также заменяет значения ,брендов в исходном датафрейме
    на индексы
    :param исходный датафрейм и связанная таблица countries_data:
    :return brand(id_brand, name, id_country)
    '''
    unique_brands = np.unique(site_data['brand'])
    brands_data = pd.DataFrame({'name': unique_brands})
    brands_data.index.to_list()
    countries = []
    for brand in brands_data['name']:
        countries.append(get_country_from_brand(brand))
    brands_data = brands_data.assign(country=countries)
    brands_data['country'].replace(list(countries_data['name']), countries_data.index.to_list(), inplace=True)
    site_data['brand'].replace(unique_brands, brands_data.index.to_list(), inplace=True)
    return brands_data


def make_category_data(site_data):
    '''
    также заменяет значения ,категорий в исходном датафрейме
    на индексы
    :param исходный датафрейм:
    :return category(id_category, name)
    '''
    unique_categories = np.unique(site_data['category'])
    categories_data = pd.DataFrame({'name': unique_categories})
    site_data['category'].replace(unique_categories, categories_data.index.to_list(), inplace=True)
    return categories_data


def make_product_data(site_data):
    '''
        в предыдущих методах мы заменили все значения столбцов на индексы
        осталось только удалить столбец 'country'
        :param site_data:
        :return: prod_data
        '''
    del site_data['country']
    prod_data = site_data
    return prod_data


def save_all_to_bigquery(site_data, credentials=credentials, private_key=private_key
                         , project_id=project_id):
    '''
    Вызываем все методы, которые опысанны выше и
    загружаем все на bigquery
    :param site_data:
    :return: done
    '''
    try:
        del site_data["Unnamed: 0"]
    except KeyError:
        pass

    site_data.to_gbq('site_parsing.site_data', if_exists='replace',
                     project_id=project_id, private_key=private_key)

    country_data = make_country_data(site_data)
    country_data.to_gbq('site_parsing.country_data', if_exists='replace',
                        project_id=project_id, private_key=private_key)

    brand_data = make_brands_data(site_data, country_data)
    brand_data.to_gbq('site_parsing.brand_data', if_exists='replace',
                        project_id=project_id, private_key=private_key)

    category_data = make_category_data(site_data)
    category_data.to_gbq('site_parsing.category_data', if_exists='replace',
                        project_id=project_id, private_key=private_key)

    product_data = make_product_data(site_data)
    product_data.to_gbq('site_parsing.product_data', if_exists='replace',
                        project_id=project_id, private_key=private_key)


def get_site_data(credentials=credentials,
             private_key=private_key, project_id=project_id):
    '''
    Дергаем из bigquery dataframe
    :return: site_data
    '''
    # Query
    query = '''
    SELECT category, brand, price
    FROM site_parsing.site_data
    '''
    site_data = pd.read_gbq(query, project_id=project_id, credentials=credentials, dialect="legacy")
    return site_data
