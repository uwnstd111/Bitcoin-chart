import math
import re
from urllib.request import urlopen
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from constants import *
from twisted.internet import task, reactor
from main import content_df, list_col_names, request_site
import mplcyberpunk


def loop_price():
    refresh_price('td', 'th', 'first left bold noWrap', 'redFont', 'greenFont')
    pass


def refresh_price(*args):
    html = urlopen(request_site).read()
    bs = BeautifulSoup(html, 'html.parser')
    rows = bs.find_all('tr')
    if args[4] in str(rows[1]):
        cena = rows[1].find(args[0], class_=args[4])
        print(cena)
    else:
        cena = rows[1].find(args[0], class_=args[3])

    if cena is not None:
        cena = re.findall("[0-9]+", str(cena.attrs))
        if cena and len(cena) > 2:
            cena = float(cena[0] + cena[1] + "." + cena[2])
        set_actual_price_text(cena, open_price)


def set_actual_price_text(close_price, open_price):
    ax = fig.gca()
    if close_price < open_price:
        ax.annotate(y[0], xy=(actual_x_index, y[0]), bbox={'facecolor': chart_colors[0], 'alpha': 0.75, 'pad': 2})
        plt.axhline(y=y[0], linestyle='-.', color=chart_colors[0])
    else:
        ax.annotate(y[0], xy=(actual_x_index, y[0]),
                    bbox={'facecolor': chart_colors[1], 'alpha': 0.75, 'pad': 2})
        plt.axhline(y=y[0], linestyle='-.', color=chart_colors[1])

    plt.show()
    plt.pause(10)


def MovingAverage():
    for ind in range(0, 3):
        if MA_iter[ind] < len(y):
            plt.plot(x1[MA_iter[ind] - 1:len(x2[ind]) + MA_iter[ind]], x2[ind])
        else:
            print("Średnia krocząca nie może przekraczać ilości świec")


def moving_average(x, w):
    return np.convolve(x, np.ones(w), 'valid') / w


def initiate_bars(df, width, width2, col1, col2):
    down = content_df[df[list_col_names[2]] >= df[list_col_names[3]]]
    up = content_df[df[list_col_names[2]] < df[list_col_names[3]]]
    plt.bar(up[list_col_names[0]], up[list_col_names[2]] - up[list_col_names[3]], width, bottom=up[list_col_names[3]],
            color=col1)
    plt.bar(up[list_col_names[0]], up[list_col_names[4]] - up[list_col_names[2]], width2, bottom=up[list_col_names[2]],
            color=col1)
    plt.bar(up[list_col_names[0]], up[list_col_names[5]] - up[list_col_names[3]], width2, bottom=up[list_col_names[3]],
            color=col1)

    plt.bar(down[list_col_names[0]], down[list_col_names[2]] - down[list_col_names[3]], width,
            bottom=down[list_col_names[3]],
            color=col2)
    plt.bar(down[list_col_names[0]], down[list_col_names[4]] - down[list_col_names[3]], width2,
            bottom=down[list_col_names[3]],
            color=col2)
    plt.bar(down[list_col_names[0]], down[list_col_names[5]] - down[list_col_names[2]], width2,
            bottom=down[list_col_names[2]],
            color=col2)


def gaussian(x, a, b, c, d=0):
    return a * math.exp(-(x - b) ** 2 / (2 * c ** 2)) + d


# create figure
fig = plt.figure()
fig.patch.set_facecolor('black')
plt.style.use("cyberpunk")
initiate_bars(content_df, .4, .05, chart_colors[0], chart_colors[1])
x = content_df[list_col_names[1]]
x1 = pd.Series(np.arange(0, 32, 1, dtype=int))  # .to_numpy()
y = content_df[list_col_names[2]]
y1 = content_df[list_col_names[2]].to_numpy()
x2 = [moving_average(y, MA_iter[0]), moving_average(y, MA_iter[1]), moving_average(y, MA_iter[2])]
y_min = content_df[list_col_names[5]].min()
y_max = content_df[list_col_names[4]].max()
open_price = content_df[list_col_names[3]][0]
print(len(x1))
print(len(y1))

plt.xticks(rotation=45, ha='right')
plt.plot(x, y, linestyle='--')
if len(x1) == len(y1):
    z = np.polyfit(x1, y1, 8)
    p = np.poly1d(z)
    MovingAverage()
    plt.plot(x1, p(x1))
plt.grid(True)
plt.ion()
# looping
loop = task.LoopingCall(loop_price)
loop.start(timeout)
reactor.run()
