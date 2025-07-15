import ccxt
import json
import os

class ExchangeManager:
    def __init__(self, config, testMode=False):
        self.config = config
        self.testMode = testMode
        self.exchange = self.connectExchange()
        self.markets = self.loadMarkets()

    def connectExchange(self):
        opts = {
            'apiKey': self.config["apiKey"],
            'secret': self.config["apiSecret"],
            'enableRateLimit': True,
            'options': {'defaultType': 'swap'}
        }
        if self.testMode:
            opts['options']['sandboxMode'] = True
            opts['urls'] = {'api': {'swap': 'https://open-api-swap.bingx.com/sandbox'}}
        return ccxt.bingx(opts)

    def loadMarkets(self):
        marketsPath = "files/json/markets.json"
        if os.path.exists(marketsPath):
            with open(marketsPath, "r", encoding="utf-8") as f:
                return json.load(f)
        else:
            markets = self.exchange.load_markets()
            with open(marketsPath, "w", encoding="utf-8") as f:
                json.dump(markets, f, indent=2)
            return markets

    def getPerpetualFutures(self):
        return [symbol for symbol, info in self.markets.items() if info.get('type') == 'swap' and info.get('contractType', '').lower() == 'perpetual']

    def fetchOhlcv(self, symbol, limit=150):
        return self.exchange.fetch_ohlcv(symbol, timeframe='1m', limit=limit)

    def fetchTicker(self, symbol):
        return self.exchange.fetch_ticker(symbol)

    def fetchPositions(self):
        return self.exchange.fetch_positions()

    def createOrder(self, **kwargs):
        return self.exchange.create_order(**kwargs)
