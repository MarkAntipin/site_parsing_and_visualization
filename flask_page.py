from flask import Flask, render_template, request, url_for, redirect, send_file
import os
import io, base64
import matplotlib.pyplot as plt
import pandas as pd
from site_parsing import save_links_to_file, make_dataframe
from making_dataframes import save_all_to_bigquery, get_site_data, read_data_csv
from visualization import make_fig
from azure_connection import download_to_azure, get_site_data_azure


def save_all(cloud):
    if cloud=='bigquery':
        site_data = read_data_csv("site_data.csv")
        save_all_to_bigquery(site_data)
        return pd.read_csv("site_data.csv")
        pass
    elif cloud=='azure':
        download_to_azure("site_data.csv")
        return pd.read_csv("site_data.csv")



def get_all(cloud):
    if cloud=='bigquery':
        return get_site_data()
    elif cloud=='azure':
        return get_site_data_azure()


app = Flask(__name__)


@app.route('/', methods=["GET",'POST'])
def hello_world():
    choices = ["heatmap","hist"]
    choices2 = ["bigquery","azure"]
    if request.method=="POST":
        graph = request.form.get('choices',None)
        vendor = request.form.get('vendors',None)
        source = request.form.get('source',None)
        if graph is not None:
            plt.clf()
            output = io.BytesIO()
            dataset = get_all(vendor)
            make_fig(dataset, graph)
            plt.savefig(output, format='png')
            plot_url = base64.b64encode(output.getvalue()).decode()
            return '<img src="data:image/png;base64,{}">'.format(plot_url)
        elif source is not None:
            save_all(source)
            return "База обновлена"
    return render_template('index.html', choices=choices, choices2=choices2, vendors=choices2)


if __name__ == '__main__':
    app.run()

