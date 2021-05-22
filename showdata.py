import time
from flask import Flask, render_template, send_file
from analizeData import analyze, readData, plotdata, norte as dfnorte
from io import BytesIO, StringIO
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib.pyplot as plt
import webbrowser
import json
import base64
app = Flask(__name__, template_folder='./')


columns = [
    {
        "field": "title",  # which is the field's name of data key
        "title": "title",  # display as the table header's name
        "sortable": True,
    },
    {
        "field": "price",
        "title": "price",
        "sortable": True,
    },
    {
        "field": "mts",
        "title": "mts",
        "sortable": True,
    },
    {
        "field": "rooms",
        "title": "rooms",
        "sortable": True,
    }, {
        "field": "baths",
        "title": "baths",
        "sortable": True,
    }, {
        "field": "parking",
        "title": "parking",
        "sortable": True,
    },
    {
        "field": "url",
        "title": "url",
        "sortable": True,
    },

]


@app.route('/')
def home():
    return render_template('./templates/index.html')


@app.route('/norte')
def norte():
    with open("./data/norte.json", 'rb') as f:
        data = json.load(f)
    return render_template('./templates/norte.html', data=data,
                           columns=columns,
                           title='NORTE')


@app.route('/sur')
def sur():
    with open("./data/sur.json", 'rb') as f:
        data = json.load(f)
    return render_template('./templates/sur.html', data=data,
                           columns=columns,
                           title='SUR')


@app.route('/oeste')
def oeste():
    with open("./data/oeste.json", 'rb') as f:
        data = json.load(f)
    return render_template('./templates/oeste.html', data=data,
                           columns=columns,
                           title='oeste')


@app.route('/oriente')
def oriente():
    with open("./data/oriente.json", 'rb') as f:
        data = json.load(f)
    return render_template('./templates/oriente.html', data=data,
                           columns=columns,
                           title='oriente')


@app.route('/centro')
def centro():
    with open("./data/centro.json", 'rb') as f:
        data = json.load(f)
    return render_template('./templates/centro.html', data=data,
                           columns=columns,
                           title='centro')


if __name__ == '__main__':
    # import webbrowser

    # def countdown(t):
    #     while t:
    #         mins, secs = divmod(t, 60)
    #         timer = '{:02d}:{:02d}'.format(mins, secs)
    #         print(timer, end="\r")
    #         time.sleep(1)
    #         t -= 1

    # print('Fire in the hole!!')

    # webbrowser.open("http://127.0.0.1:5000/")
    app.run(debug=True)
