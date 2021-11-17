import alpaca_trade_api as tradeapi
import time
import urllib3

urllib3.disable_warnings(urllib3.exceptions.HTTPWarning)

api=None
_L=None



def waitIfMarketIsClosed(isForSell=False):
    wasMarketOpen=True
    while True:
        clock = api.get_clock()
        if clock.is_open:
            if (wasMarketOpen==False):
                if (not isForSell):
                    _L.info("The market is open now but still waiting for 31 minutes to start trading...")
                    time.sleep(31*60)
                else:
                    _L.info("Dont wait cause sell is important to be done instantly")
            return wasMarketOpen
        else:
            if (wasMarketOpen==True):
                _L.info("The market is closed.. waiting until the market opens again...")
            wasMarketOpen=False
            time.sleep(120)