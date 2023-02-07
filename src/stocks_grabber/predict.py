import pandas as pd
from fbprophet import Prophet
import yfinance as yf
import warnings
from cachetools import cached, TTLCache
from cache_to_disk import cache_to_disk

cache = TTLCache(maxsize=100, ttl=3600)


@cached(cache)
def get_data(symbol):
    return yf.download(symbol)


def remove_tz(item):
    return item.replace(tzinfo=None)


@cache_to_disk(1)
def get_forecast_and_history_df(symbol='AAPL'):
    warnings.simplefilter('ignore')
    prediction_period = '5Y'
    data = get_data(symbol)

    df = pd.DataFrame()
    df['ds'] = data.index.get_level_values('Date')
    df['y'] = data['Close'].values
    df['ds'] = df['ds'].apply(remove_tz)

    df = df.resample('W', on='ds').mean()
    df['ds'] = df.index
    df = df.dropna()

    m = Prophet()
    m.fit(df)

    # predictions
    future = m.make_future_dataframe(periods=int(prediction_period[:-1]), freq=prediction_period[-1])
    forecast = m.predict(future)
    return df, forecast


def pickle_data(df, forecast, symbol):
    df.to_pickle(f'data/{symbol}-history')
    forecast.to_pickle(f'data/{symbol}-forecast')


def run_forecaster(symbol):
    df, forecast = get_forecast_and_history_df(symbol)
    pickle_data(df, forecast, symbol)


def is_stock_ready(symbol):
    import os
    return os.path.exists(f'data/{symbol}-history') and os.path.exists(f'data/{symbol}-forecast')


if __name__ == '__main__':
    import time
    start = time.time()
    history, forecast = get_forecast_and_history_df('AAPL')
    print(len(forecast), time.time()-start)
    print(forecast.tail(3))
# 10623 2023-12-31  160.990342  ...                         0.0  161.201754
# 10624 2024-12-31  178.134514  ...                         0.0  178.384774
# 10625 2025-12-31  195.231845  ...                         0.0  195.494060
