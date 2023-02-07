import os

import scrapy


class StocksSymbolsSpider(scrapy.Spider):
    name = 'stocks_symbols'
    path = os.path.join(name)
    custom_settings = {
        'FEEDS': {
            'data.json': {'format': 'json', 'overwrite': True}
        }
    }
    allowed_domains = ['stockanalysis.com']
    start_urls = ['https://stockanalysis.com/stocks/']

    def parse(self, response):
        import re
        import json
        script_el = response.css("script[type=module]::text")[0]
        script_text = script_el.get()
        json_text = re.search("data:(\[{.*?}])},", script_text)[1]
        json_text = self.fix_text_json(json_text)
        data = json.loads(json_text)
        for stock in data:
            yield dict(
                symbol=stock['s'],
                name=stock['n'],
                industry=stock['i'],
                market_cap=stock['m']
            )

    @staticmethod
    def fix_text_json(text):
        fixes = [
            ('s:', '"s":'),
            ('i:', '"i":'),
            ('n:', '"n":'),
            ('m:', '"m":'),
        ]
        for to_replace, replacement in fixes:
            text = text.replace(to_replace, replacement)
        return text

    def save(self, text):
        with open(self.path, 'w') as f:
            f.write(text)
