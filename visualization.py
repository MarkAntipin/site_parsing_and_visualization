'''
Здесь будет визуализация для отчета
по мере увеличения задания будет дополняться
'''

from making_dataframes import get_site_data
import collections
import pandas as pd
import matplotlib.pyplot as plt


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
