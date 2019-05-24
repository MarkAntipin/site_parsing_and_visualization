from flask import Flask, render_template, request, url_for, redirect, send_file
import os
import io, base64
import matplotlib.pyplot as plt
from visualization import pivot_table, heat_map

app = Flask(__name__)

@app.route('/', methods=["GET",'POST'])
def hello_world():
    choices = ["heatmap","hist"]
    if request.method=="POST":
        graph=request.form.get('choices', None)
        print(graph)
        if graph is not None:
            plt.clf()
            output = io.BytesIO()
            # make_fig(graph)
            plt.savefig(output,format='png')
            plot_url = base64.b64encode(output.getvalue()).decode()
            return '<img src="data:image/png;base64,{}">'.format(plot_url)
    return render_template('index.html', choices=choices)


@app.route('/pivot')
def pivot():
    pivot_table()
    return send_file('images/pivot.png')


@app.route('/heat')
def pivot():
    heat_map()
    return send_file('images/heat_map.png')


@app.route('/update')
def update():

    return redirect('/')


if __name__ == '__main__':
    app.run()
