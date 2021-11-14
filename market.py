import alpaca_trade_api as tradeapi
import time
import urllib3

urllib3.disable_warnings(urllib3.exceptions.HTTPWarning)

api=None
_L=None



def waitIfMarketIsClosed():
    wasMarketOpen=True
    while True:
        clock = api.get_clock()
        if clock.is_open:
            if (wasMarketOpen==False):
                _L.info("The market is open now but still waiting for 31 minutes to start trading...")
                time.sleep(31*60)
            return wasMarketOpen
        else:
            if (wasMarketOpen==True):
                _L.info("The market is closed.. waiting until the market opens again...")
            wasMarketOpen=False
            time.sleep(120)