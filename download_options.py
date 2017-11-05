from pandas_datareader.data import Options
import pandas as pd
import pytz
import datetime
import os
import sys
from tickers import tickers

def get_opts(ticker, nb_months=3):
    opts = Options(ticker, 'yahoo')
    data = opts.get_forward_data(nb_months, put=True)
    return data

def analysis(df):
    df['mid_price'] = df.loc[:, ['Ask','Bid']].mean(axis=1)
    df['mid_price_fraction'] = df['mid_price']/df['Underlying_Price']
    df['strike'] = df.index.get_level_values(0)
    df['type'] = df.index.get_level_values(2)
    df['strike_price_fraction'] = df['strike']/df['Underlying_Price']
    return df

df = pd.DataFrame()
for ticker in tickers:
    opts = get_opts(ticker)
    opts['ticker'] = opts['Root']
    opts = analysis(opts)
    df = df.append(opts)

fn = pd.datetime.now(pytz.timezone('America/New_York')).strftime("%Y%m%d_%H%M%S.p")
fpath = os.path.abspath(os.sep.join(sys.argv[0].split(os.sep)[:-1]) + os.sep.join(["", "data", fn]))
df.to_pickle(fpath)