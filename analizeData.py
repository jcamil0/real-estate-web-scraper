# -*- coding: utf-8 -*-
import pandas as pd
import json
import numpy as np
# from matplotlib import pyplot as plt
import matplotlib.pyplot as plt


def readData(zone):
    data = []
    with open('./data/' + zone + ".json", 'rb') as f:
        data = json.load(f)
        df = pd.DataFrame(data)
    return df


def norte():
    df_norte = readData('norte')
    df_norte['item'] = 'norte'
    return df_norte


def sur():
    df_sur = readData('sur')
    df_sur['item'] = 'sur'
    return df_sur


def oeste():
    df_oeste = readData('oeste')
    df_oeste['item'] = 'oeste'

    return df_oeste


def oreinte():
    df_orinete = readData('oriente')
    df_orinete['item'] = 'oriente'

    return df_orinete


def centro():
    df_centro = readData('centro')
    df_centro['item'] = 'centro'

    return df_centro


def join_dfs():
    norte_df = norte()
    sur_df = sur()
    oeste_df = oeste()
    centro_df = centro()
    oriente_df = oreinte()

    # print(norte_df.to_html())

    frames = [
        norte_df,
        sur_df,
        oeste_df,
        centro_df,
        oriente_df,
    ]

    norte_df.groupby(['title', 'price'],).size(
    ).unstack().plot(kind='bar', stacked=True)

    fig = plt.gcf()
    fig.set_size_inches((8.5, 11), forward=False)
    fig.savefig('./templates/assets/norte.png', dpi=500)

    oriente_df.groupby(['title', 'price']).size(
    ).unstack().plot(kind='bar', stacked=True)

    fig = plt.gcf()
    fig.set_size_inches((8.5, 11), forward=False)
    fig.savefig('./templates/assets/oriente.png', dpi=500)

    centro_df.groupby(['title', 'price']).size(
    ).unstack().plot(kind='bar', stacked=True)

    fig = plt.gcf()
    fig.set_size_inches((8.5, 11), forward=False)
    fig.savefig('./templates/assets/centro_df.png', dpi=500)

    oeste_df.groupby(['title', 'price']).size(
    ).unstack().plot(kind='bar', stacked=True)

    fig = plt.gcf()
    fig.set_size_inches((8.5, 11), forward=False)
    fig.savefig('./templates/assets/oeste.png', dpi=500)

    sur_df.groupby(['title', 'price']).size(
    ).unstack().plot(kind='bar', stacked=True)

    fig = plt.gcf()
    fig.set_size_inches((8.5, 11), forward=False)
    fig.savefig('./templates/assets/sur.png', dpi=500)

    house_df = pd.concat(frames, ignore_index=True)
    return house_df


def analyze():
    housemates_df = join_dfs()

    # Number of Fans
    houses_prices = housemates_df.groupby(
        'title')['price'].count().reset_index()
    houses_prices.columns = ['item', 'price']

    mts_price = housemates_df.groupby(
        'mts')['price'].count().reset_index()
    houses_prices.columns = ['item', 'price']

    mts_prices = housemates_df.groupby(
        'mts')['price'].count().reset_index()
    houses_prices.columns = ['item', 'price']

    return (houses_prices, mts_price, mts_prices)


def plotdata():

    analysis_details = analyze()
    fans_by_housemate, fans_by_location, _ = analysis_details

    fig1, ax1 = plt.subplots()
    ax1.bar(fans_by_housemate['item'],
            fans_by_housemate['price'], label='fans by item')
    ax1.set_xlabel('item')
    ax1.set_ylabel('twitter Fans')
    ax1.set_title(' Twitter Fans  item')

    fig1, ax2 = plt.subplots()
    ax2.bar(fans_by_location['mts'],
            fans_by_location['price'], label='fans by item')
    ax2.set_xlabel('item')
    ax2.set_ylabel('twitter Fans')
    ax2.set_title(' Twitter Fans  item')

    # fans_by_location.groupby(['item', 'price']).size(
    # ).unstack().plot(kind='bar', stacked=True)

    # plt.show()

    list_of_figures = [plt.figure(i) for i in plt.get_fignums()]
    return list_of_figures
