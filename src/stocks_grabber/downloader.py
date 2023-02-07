import json
from concurrent import futures

from predict import get_forecast_and_history_df

def process_and_save(symbol):
    df, forecast = get_forecast_and_history_df(symbol)
    df.to_json(f'data/{symbol}-history.json')
    forecast.to_json(f'data/{symbol}-forecast.json')

if __name__ == '__main__':
    with open('data.json', 'r') as f:
        symbols = json.loads(f.read())
    symbols = [item['symbol'] for item in symbols]

    with futures.ProcessPoolExecutor() as executor:
        executor.map(process_and_save, symbols)
