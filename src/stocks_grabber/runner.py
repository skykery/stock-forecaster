import os.path
import logging

logger = logging.getLogger()


class Error:
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


def is_older_than_hours(file_path, hours=6):
    if not os.path.exists(file_path):
        logger.info("The file does not exist, a new one can be created.")
        return True

    import datetime
    now = datetime.datetime.now()
    modif_time = os.path.getmtime(file_path)
    return datetime.datetime.fromtimestamp(modif_time) < now - datetime.timedelta(hours=hours)


def get_stock_history(stock_symbol):
    import os
    import json
    from scrapy.crawler import CrawlerProcess
    from stocks_grabber.spiders import stock_history

    folder_to_save = 'data'
    file_path = os.path.join(folder_to_save, f'{stock_symbol}_history.json')

    if is_older_than_hours(file_path):
        logger.info("Getting fresh data from source")
        custom_settings = {
            'FEEDS': {
               file_path: {'format': 'json', 'overwrite': True}
            },
            'USER-AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        }

        from scrapy.utils.project import get_project_settings
        project_settings = get_project_settings()
        project_settings.setdict(custom_settings)
        process = CrawlerProcess(project_settings)
        process.crawl(stock_history.StockHistorySpider, stock_symbol=stock_symbol)
        process.start()

    try:
        with open(file_path, 'r') as f:
            return json.loads(f.read())
    except json.decoder.JSONDecodeError:
        return Error("Symbol not found").__dict__


def get_history(symbol):
    from concurrent import futures

    with futures.ProcessPoolExecutor() as executor:
        future = executor.submit(get_stock_history, symbol)

    return future.result()


if __name__ == '__main__':
    get_stock_history('test')
