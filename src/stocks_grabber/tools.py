import pandas as pd
from pandas import DataFrame


def load_data():
    def name_w_symbol_value(row):
        return f'{row["symbol"]} - {row["name"]}'
    df = pd.read_json("data.json")
    df['name_w_symbol'] = df.apply(lambda row: name_w_symbol_value(row), axis=1)
    return df


def get_data(df: DataFrame, substring: str):
    results = df[df['name_w_symbol'].str.contains(substring, case=False)]
    return results.to_dict('records')


def resample_df(df, date_key):
    import pandas as pd

    date_key = date_key or 'ds'
    df[date_key] = df[date_key].apply(lambda x: str(x.isoformat()))
    df[date_key] = pd.to_datetime(df[date_key])
    print(len(df[date_key]))
    df = df.resample('M', on='ds').mean()
    df['ds'] = df.index
    df = df.dropna()
    print(len(df[date_key]))
    return df
