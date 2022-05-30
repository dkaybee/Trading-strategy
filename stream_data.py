import secret
import fxcmpy
import datetime as dt
import pandas as pd
import time

# con = fxcmpy.fxcmpy(access_token=secret.token, log_level='error', log_file=None)
#
#
# def subscribe():
#     stocks=['EUR/USD','XAU/USD']   #instruments to be subscribed
#     for stock in stocks:
#         con.subscribe_market_data(stock)
#
# subscribe()
#
# def check_subscribe(instrument):
#     if con.is_subscribed(instrument)==True:
#         print("Instrument is subscribed")
#     else:
#         print("Instrument not subscribed")
#
# check_subscribe('XAU/USD')
# #get prices
#
# i=1
# while i==1:
#     con.set_max_prices(1000000)
#     kb=con.get_prices('XAU/USD')
#     kb.to_csv('stock data.csv', mode='w', header= True, index= True)
#     time.sleep(60)
#
#






