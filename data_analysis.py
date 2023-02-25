import numpy as np
import pandas as pd
from main import content_df, plt, list_col_names
import mplcyberpunk
import math
from PIL import Image
import sys


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
    print(f"Up:{up}")
    print(f"Down:{down}")
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
    return a * math.exp(-(x - b)**2 / (2 * c**2)) + d


# def load_image(path=sys.argv[1]):
#     image = Image.open(path)
#     im = image.load()
#     SIZE = image.size
#     return im


# create figure
fig = plt.figure()
fig.patch.set_facecolor('black')

#   plt.savefig(load_image(), facecolor=fig.get_facecolor(), transparent=True)
plt.style.use("cyberpunk")
initiate_bars(content_df, .4, .05, 'red', 'green')
x = content_df[list_col_names[1]]
x1 = pd.Series(np.arange(0, 32, 1, dtype=int))  # .to_numpy()
y = content_df[list_col_names[2]]
y1 = content_df[list_col_names[2]].to_numpy()
y_min = content_df[list_col_names[5]].min()
y_max = content_df[list_col_names[4]].max()
d = y_max - y[0]
dy = y_max - y_min
threshold = 0.015
fig.text(0.9035, 1 - d / dy + threshold, str(y[0]), fontsize=9, bbox={'facecolor': 'red', 'alpha': 0.75, 'pad': 2})
MA_iter = [7, 10, 21]
x2 = [moving_average(y, MA_iter[0]), moving_average(y, MA_iter[1]), moving_average(y, MA_iter[2])]
z = np.polyfit(x1, y1, 8)
p = np.poly1d(z)

MovingAverage()
plt.xticks(rotation=45, ha='right')
print(x)
print(y[len(y) - 1])
plt.plot(x, y, linestyle='--')
plt.axhline(y=y[0], linestyle='-.')
# fig.canvas.mpl_connect('close_event', on_close)

# plt.text(0.35, 0.5, 'Close Me!', dict(size=30))
plt.plot(x1, p(x1))
plt.grid(True)
plt.show()
