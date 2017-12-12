import codecs
import datetime
import logging
from User import User
from pymongo import MongoClient
from flask import json

log = logging.getLogger("DatabaseManager")

class DatabaseManager:

    def __init__(self):
        #init db connection
        log.info("connecting to db....")
        client = MongoClient('localhost', 27017)
        self.db = client.big_project
        log.info("connected to ok")
        
    def getConnection(self):
        return self.db
        
    def findUserByOpenId(self, openid):
        if (self.db.users.find_one({"openid":openid}) == None):
            return None
        else:
            userinfo = self.db.users.find_one({"openid":openid})
            return User(userinfo)
        
    def findUserByName(self, name):
        if (self.db.users.find_one({"nickname":name}) == None):
            return None
        else:
            userinfo = self.db.users.find_one({"nickname":name})
            return User(userinfo)
    
    def getPortfolios(self, user):
        tday = datetime.datetime.now()
        datestr = tday.strftime("%Y-%m-%d")
        log.info("trying to get portfolio list user : %s ", user)
        '''
        try:
            stocks = db.stocks.find({"load_date":datestr})
            stocksList = []
            for stock in stocks:
                #print stock
                stockItem = {  'load_date':stock['load_date'],
                               'stock_code':stock['stock_code'],
                               'name':stock['name'],
                               'industry':stock['industry'],
                               'area':stock['area'],
                               'pe':stock['pe'],
                               'outstanding':stock['outstanding'],
                               'totals':stock['totals'],
                               'totalAssets':stock['totalAssets'],
                               'liquidAssets':stock['liquidAssets'],
                               'fixedAssets':stock['fixedAssets'],
                               'reserved':stock['reserved'],
                               'reservedPerShare':stock['reservedPerShare'],
                               'esp':stock['esp'],
                               'bvps':stock['bvps'],
                               'pb':stock['pb'],
                               'timeToMarket':stock['timeToMarket'],
                               'undp':stock['undp'],
                               'perundp':stock['perundp'],
                               'rev':stock['rev'],
                               'profit':stock['profit'],
                               'gpr':stock['gpr'],
                               'npr':stock['npr'],
                               'holders':stock['holders'],
                               'id':str(stock['_id'])}
                stocksList.append(stockItem)
        '''
        try:
            with codecs.open("static/data/portfolios.js", encoding="utf-8") as json_data:
                data = json_data.read()
                data = json.loads(data)
                log.info(data)
        except Exception as e:
            log.error(e)
        return json.dumps(data)