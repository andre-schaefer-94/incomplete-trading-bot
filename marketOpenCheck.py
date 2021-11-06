import alpaca_trade_api as tradeapi
import time

api=None
_L=None
def waitIfMarketIsClosed():
    wasMarketOpen=True
    while True:
        clock = api.get_clock()
        if clock.is_open:
            return wasMarketOpen
        else:
            _L.info("The market is closed.. waiting until the market opens again...")
            wasMarketOpen=False
            time.sleep(120)