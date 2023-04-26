import re
from typing import Any
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from constants import *
from numpy import ndarray
from pandas import DataFrame, Series
from twisted.internet import task, reactor


def init_fig(content_df: DataFrame, col_names: list[str], request_site: Request) -> None:
    # create figure
    fig = plt.figure()
    fig.patch.set_facecolor('black')
    import mplcyberpunk
    plt.style.use("cyberpunk")
    initiate_bars(content_df, .4, .05, chart_colors[0], chart_colors[1], col_names)
    x = content_df[col_names[1]]
    x1 = pd.Series(np.arange(0, 32, 1, dtype=int))  # .to_numpy()
    y = content_df[col_names[2]]
    y1 = content_df[col_names[2]].to_numpy()
    x2 = [moving_average(y, MA_iter[0]), moving_average(y, MA_iter[1]), moving_average(y, MA_iter[2])]
    # y_min = content_df[col_names[5]].min()
    # y_max = content_df[col_names[4]].max()
    open_price = content_df[col_names[3]][0]

    plt.xticks(rotation=45, ha='right')
    plt.plot(x, y, linestyle='--')
    if len(x1) == len(y1):
        z = np.polyfit(x1, y1, 8)
        p = np.poly1d(z)
        MovingAverage(x1, x2, y)
        plt.plot(x1, p(x1))
    plt.grid(True)
    plt.ion()
    # looping
    loop = task.LoopingCall(lambda: loop_price(open_price, fig, y, request_site))
    loop.start(timeout)
    reactor.run()


def loop_price(open_price: DataFrame, fig: Any, y: DataFrame, request_site: Request) -> None:
    refresh_price(open_price, fig, y, request_site, 'td', 'th', 'first left bold noWrap', 'redFont', 'greenFont')
    pass


def get_fresh_data(request_site: Request) -> ResultSet:
    html = urlopen(request_site).read()
    bs = BeautifulSoup(html, 'html.parser')
    data_set = bs.find_all('tr')
    return data_set


def refresh_price(open_price: DataFrame, fig: Any, y: DataFrame, request_site: Request, *args: (str, ...)) -> None:
    rows = get_fresh_data(request_site)
    if args[4] in str(rows[1]):
        price = rows[1].find(args[0], class_=args[4])
    else:
        price = rows[1].find(args[0], class_=args[3])

    if price is not None:
        price = re.findall("[0-9]+", str(price.attrs))
        if price and len(price) > 2:
            price = float(price[0] + price[1] + "." + price[2])
        set_actual_price_text(price, open_price, fig, y)


def set_actual_price_text(close_price: Any, open_price: DataFrame, fig: Any, y: DataFrame) -> None:
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


def MovingAverage(x1: Series, x2: list, y: DataFrame) -> None:
    for ind in range(0, 3):
        if MA_iter[ind] < len(y):
            plt.plot(x1[MA_iter[ind] - 1:len(x2[ind]) + MA_iter[ind]], x2[ind])
        else:
            print("Średnia krocząca nie może przekraczać ilości świec")


def moving_average(x: DataFrame, w: list[int]) -> ndarray:
    return np.convolve(x, np.ones(w), 'valid') / w


def initiate_bars(df: DataFrame, width: float, width2: float, col1: str, col2: str, col_names: list[str]) -> None:
    down = df[df[col_names[2]] >= df[col_names[3]]]
    up = df[df[col_names[2]] < df[col_names[3]]]
    plt.bar(up[col_names[0]], up[col_names[2]] - up[col_names[3]], width, bottom=up[col_names[3]],
            color=col1)
    plt.bar(up[col_names[0]], up[col_names[4]] - up[col_names[2]], width2, bottom=up[col_names[2]],
            color=col1)
    plt.bar(up[col_names[0]], up[col_names[5]] - up[col_names[3]], width2, bottom=up[col_names[3]],
            color=col1)

    plt.bar(down[col_names[0]], down[col_names[2]] - down[col_names[3]], width,
            bottom=down[col_names[3]],
            color=col2)
    plt.bar(down[col_names[0]], down[col_names[4]] - down[col_names[3]], width2,
            bottom=down[col_names[3]],
            color=col2)
    plt.bar(down[col_names[0]], down[col_names[5]] - down[col_names[2]], width2,
            bottom=down[col_names[2]],
            color=col2)
