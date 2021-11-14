# encoding: utf-8

# This code is free, THANK YOU!
# It is explained at the guide you can find at www.theincompleteguide.com
# You will also find improvement ideas and explanations

from datetime import date

import gvars


class Stock:

    def __init__(self,name='INIT', purchaseDate=date.today()):
        self.name = name
        self.currentPrice = 0
        self.direction = ''
        self.purchaseDate = purchaseDate

    def set_name(self,name):
        self.name = name

    def patternDayTradeProtectionSELL(self):
        if (not gvars.PATTERN_DAY_TRADE_PROTECTION):
            return True
        if ((date.today()-self.purchaseDate).days>=1):
            return True
        else:
            return False
