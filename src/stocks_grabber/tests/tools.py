from unittest import TestCase, mock

from stocks_grabber.tools import load_data, get_data

data = [
    {"symbol": "A", "name": "Agilent Technologies, Inc."},
    {"symbol": "AA", "name": "Alcoa Corporation"},
]


def get_df(data):
    import pandas as pd
    return pd.DataFrame(data)


class ToolsTestCase(TestCase):
    def test_load_data(self):
        with mock.patch('pandas.read_json', return_value=get_df(data)):
            self.assertEqual(load_data()['name_w_symbol'][0], '(A) Agilent Technologies, Inc.')

    def test_get_data(self):
        with mock.patch('pandas.read_json', return_value=get_df(data)):
            df = load_data()
        result = get_data(df, 'agile')
        self.assertEqual(result, [df.to_dict('records')[0]])
