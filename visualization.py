'''
Здесь будет визуализация для отчета
по мере увеличения задания будет дополняться
'''

from making_dataframes import get_site_data
import collections
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from azure_connection import get_site_data_azure


def pivot_table():
    '''
    сохраняет pivot table по брендам
    '''
    site_data = get_site_data()
    brands_counter = collections.Counter()
    for i in site_data['brand']:
        brands_counter[i] += 1

    brands_counter_1 = dict()
    for i in brands_counter.keys():
        if brands_counter[i] > 2:
            brands_counter_1[i] = brands_counter[i]

    brands_data = pd.DataFrame(brands_counter_1.items(), columns=['brand', 'counter'])

    pivot = brands_data.pivot_table(index='brand').plot.bar(rot=0, stacked=True)
    fig = pivot.get_figure()
    fig.savefig("images/pivot.png")


def heat_map():
    '''
    сохраняет heat map
    '''
    site_data = get_site_data_azure()

    site_data_group_1 = site_data.groupby(by=['category', 'brand'], observed=True)['price'].mean()
    prices = []
    for i in site_data_group_1:
        prices.append(i)

    brands = []
    types = []
    for i in site_data_group_1.keys():
        brands.append(i[1])
        types.append(i[0])

    site_data_1 = pd.DataFrame({'price': prices, 'brand': brands, 'category': types})
    heats = sns.heatmap(site_data_1.pivot(index='brand', columns='category')['price'])
    fig = heats.get_figure()
    fig.savefig("images/heat_map.png")
