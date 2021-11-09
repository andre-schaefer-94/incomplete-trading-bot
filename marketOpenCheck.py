import alpaca_trade_api as tradeapi
import time
import urllib3

urllib3.disable_warnings()

api=None
_L=None
def waitIfMarketIsClosed():
    wasMarketOpen=True
    while True:
        clock = api.get_clock()
        if clock.is_open:
            return wasMarketOpen
        else:
            if (wasMarketOpen==True):
                _L.info("The market is closed.. waiting until the market opens again...")
            wasMarketOpen=False
            time.sleep(120)