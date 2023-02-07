import scrapy
import io


class StockHistorySpider(scrapy.Spider):
    name = 'stock_history'
    allowed_domains = ['query1.finance.yahoo.com']

    def __init__(self, *args, **kwargs):
        stock_symbol = kwargs.get('stock_symbol', 'AAPL')
        self.start_urls = [
            f'https://query1.finance.yahoo.com/v7/finance/download/{stock_symbol}?period1=1642475224&period2=1674011224&interval=1d&events=history&includeAdjustedClose=true']
        super(StockHistorySpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        import pandas as pd
        df = pd.read_csv(io.StringIO(response.text))
        items = df.to_dict('records')
        for item in items:
            yield item

    def save(self, text):
        with open(self.name, 'w') as f:
            f.write(text)
