# encoding: utf-8

# This code is free, THANK YOU!
# It is explained at the guide you can find at www.theincompleteguide.com
# You will also find improvement ideas and explanations

import pandas as pd
from datetime import datetime
from datetime import timedelta
import time, threading, requests, re, random, os
import other_functions
from bs4 import BeautifulSoup

from market import waitIfMarketIsClosed
from other_functions import *
import gvars
import pytz
import alpaca_trade_api as tradeapi

class AssetHandler:
    def __init__(self,api):
        self.lockedAssets = set() # assets without a defined strategy
        self.tradeableAssets = set() # assets that may be traded today
        self.availableAssets = set() # assets availabe post filter
        self.usedAssets = set() # taken assets being traded
        self.excludedAssets = {'SPCE'} # excluded assets (EXAMPLE)
        self.api=api

        try:
            #ass=self.getAllAssets()
            #self.rawAssets = set(pd.read_csv(gvars.RAW_ASSETS))
            ##self.rawAssets = set(ass)
            #print("Raw assets loaded from csv correclty")
            print("Initializing AssetHandler")
        except Exception as e:
            print("Could not load raw assets!")
            print(e)
            block_thread()

        #self.tradeableAssets = self.rawAssets

        th = threading.Thread(target=self.unlock_assets) # the process runs appart
        th.start()

    def findInterestingAsset(self):
        while True:
            assets=self.api.list_assets('active')
            ass=set()
            strList=[]
            count=0
            for asset in assets:
                strList.append(asset.symbol)
                count=count+1
                if (count==200):
                    latestBars=self.api.get_barset(strList, '1Min', 1)
                    # latestTrades=self.api.get_latest_bars(strList)
                    dtNOW = datetime.now(pytz.timezone("America/New_York"))
                    for a in strList:
                        stockname = a
                        lastTrade = None
                        try:
                            lastTrade = latestBars[a]
                        except KeyError as e:
                            e = e
                        if (lastTrade == None):
                            continue
                        if (len(lastTrade)==0):
                            continue
                        if (lastTrade.df.high[0] > gvars.operEquity):
                            continue

                        timedelay = dtNOW - lastTrade[0].t
                        if (timedelay.seconds / 60 > 3):
                            continue
                        yield stockname
                    count = 0
                    strList = []
            if (len(strList) !=0):
                latestBars=self.api.get_barset(strList, '1Min',1)
            #return ass

    def find_target_asset(self):

        while True:
            #self.availableAssets = self.tradeableAssets
            #self.availableAssets -= self.usedAssets
            #self.availableAssets -= self.excludedAssets
            #self.availableAssets -= self.lockedAssets

            try:
                #chosenAsset = random.choice(list(self.availableAssets)) # pick a chosen asset randomly
                gen=self.findInterestingAsset()
                for chosenAsset in self.findInterestingAsset():
                    if chosenAsset not in self.usedAssets and chosenAsset not in self.lockedAssets:
                        break
                self.usedAssets.add(chosenAsset)
                print('Chosen asset: ' + chosenAsset)
                #print('%i available assets, %i used assets, %i locked assets\n' % (len(self.availableAssets),len(self.usedAssets),len(self.lockedAssets)))
                print('%i used assets, %i locked assets\n' % (
                len(self.usedAssets), len(self.lockedAssets)))
                return chosenAsset
            except Exception as e:
                print('No more assets available, waiting for assets to be released...')
                time.sleep(60)

    def make_asset_available(self,ticker):

        try:
            self.usedAssets.remove(ticker)
        except Exception as e:
            print('Could not remove %s from used assets, not found' % ticker)
            print(e)

        self.availableAssets.add(ticker)
        print('Asset %s was made available' % ticker)
        time.sleep(1)

    def lock_asset(self,ticker):
        if type(ticker) is not str:
            raise Exception('ticker is not a string!')

        time = datetime.now()
        self.usedAssets.remove(ticker)
        self.lockedAssets.add(ticker)

    def unlock_assets(self):
        # this function unlocks the locked assets periodically

        print('\nUnlocking service initialized')
        while True:
            waitIfMarketIsClosed()
            print('\n# # # Unlocking assets # # #\n')
            time_before = datetime.now()-timedelta(minutes=30)


            self.tradeableAssets = self.tradeableAssets.union(self.lockedAssets)
            print('%d locked assets moved to tradeable' % len(self.lockedAssets))
            self.lockedAssets = set()

            time.sleep(gvars.sleepTimes['UA'])
