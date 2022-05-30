import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.transforms as transforms
import matplotlib.ticker as mticker
from matplotlib.gridspec import GridSpec
from matplotlib.widgets import CheckButtons
from mycolorpy import colorlist as mcp
from mplfinance.original_flavor import candlestick_ohlc
import datetime
import math
import pandas as pd
import numpy as np
import pandas_ta as ta

def figure_design(axs):
    for ax in axs:
        ax.set_facecolor('#1e1e1e')
        ax.tick_params(axis='both', labelsize=10, colors='#e4e4e4')
        ax.ticklabel_format(useOffset=False)
        ax.spines['bottom'].set_color('#787878')
        ax.spines['left'].set_color('#787878')


# define the function and itll be called in the animate function
def ax_design(ax, y_axis_visible=False, x_axis_label=False):
    ax.clear()
    ax.grid(True, color='grey', linestyle='-', which='major', axis='both', linewidth=0.3)

    # y_axis_visible
    if y_axis_visible == False:
        ax.axes.yaxis.set_visible(y_axis_visible)
    else:
        ax.yaxis.set_ticks_position('right')

    # x_axis_visble
    if x_axis_label == False:
        ax.set_xticklabels([])
    else:
        ax.tick_params(axis='x', which='major', labelsize=8)

def compute_plot_OHLC(ax, data_ask):
    candle_counter= range(len(data_ask['open']))
    ohlc=[]

    for i in candle_counter:
        append_ohlc=candle_counter[i], data_ask['open'][i],data_ask['high'][i], data_ask['low'][i], data_ask['close'][i]
        ohlc.append(append_ohlc)
    candlestick_ohlc(ax, ohlc, width=0.8, colorup = '#53b987', colordown = '#eb4d5c')

    if data_ask['close'].iloc[-1] >= data_ask['open'].iloc[-1]:
        colorcode = '#53b987'
    else:
        colorcode = '#eb4d5c'

    #for horizonal lien
    ax.axhline(data_ask['close'].iloc[-1], linestyle='--', colorcode=colorcode, linewidth=0.5)

    trans= transforms.blended_transform_factory(ax.tranAxes, ax.transData)
    ax.text(1.005, data_ask['close'].iloc[-1], data_ask['close'].iloc[-1],color= '#e4e4e4', fontsize=12,
            transform=trans, horizontalalignment= 'left', verticalalignment= 'center',
            bbox=dict(facecolor=colorcode, edgecolor=colorcode))

    ########Open high low cls on graph (top right)
    strings=['O', str(data_ask['open'].iloc[-1]),
             'H', str(data_ask['high'].iloc[-1]),
             'L', str(data_ask['low'].iloc[-1]),
             'C', str(data_ask['close'].iloc[-1])]
    colors = ['#e4e4e4', colorcode,
             '#e4e4e4', colorcode,
             '#e4e4e4', colorcode,
             '#e4e4e4', colorcode ]
    margin_label=0
    margin_price=0

    for s,c in zip(strings, colors):
        ax.text(0.75 +margin_label +margin_price, 0.95, s+" ", color=c, transform=ax.transAxes,
                fontsize=12, fontweight='bold', horizontalaalignment='left',
                verticalaalignment='center')
        if c == "#e4e4e4":
            margin_label = margin_label+0.01
        else:
            margin_price = margin_price+0.05
# animation
def process_data(filename):
    df = pd.read_csv(filename, index_col=['Unnamed: 0'], parse_dates=['Unnamed: 0'])

    latest_info=df.iloc[-1,:]
    latest_bid = str(latest_info.iloc[0])
    latest_ask = str(latest_info.iloc[1])


# df=pd.read_csv("stock data.csv")
# df.dtypes
    df['Unnamed: 0'] = pd.to_datetime(df['Unnamed: 0'], format="%Y/%m/%d %H:%M:%S")

    data_ask = df['Ask'].resample('15Min').ohlc()
    data_ask['RSI'] = ta.rsi(data_ask['close'], timeperiod=14)
    data_ask['RSI'] = data_ask['RSI'].fillna(0)

    return data_ask, latest_bid, latest_ask

def animate(i):
    time_stamp = datetime.datetime.now() - datetime.timedelta(hours=12)
    time_stamp = time_stamp.strftime("%Y-%m-%d %H:%M:%S")
    filename = str(time_stamp) + 'stock data.csv'

    # Main
    ax_design(ax1, y_axis_visible=True, x_axis_label=False)

    plot_header(ax1)

    ohlc = compute_plot_OHLC(ax1, data_ask)



    # MACD
    ax_design(ax2, y_axis_visible=True, x_axis_label=False)

    # rsi
    ax_design(ax3, y_axis_visible=True, x_axis_label=True)

fig=plt.figure()
fig.patch.set_facecolor('#121416')
gs= fig.add_gridspec(10, 6)  #10 row by 6 columns grid
ax1=fig.add_subplot(gs[0:7, 0:6])
ax2=fig.add_subplot(gs[8, 0:6])
ax3=fig.add_subplot(gs[9, 0:6])
figure_design([ax1, ax2, ax3])

ani=animation.FuncAnimation(fig, animate, interval=1)
plt.show()
