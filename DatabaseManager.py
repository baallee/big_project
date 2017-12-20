import datetime
import logging
from User import User
from pymongo import MongoClient
from bson.objectid import ObjectId
from flask import json
import tushare as ts

log = logging.getLogger("DatabaseManager")

class DatabaseManager:

    def __init__(self):
        #init db connection
        log.info("connecting to db....")
        client = MongoClient("localhost", 27017)
        self.db = client.big_project
        log.info("connected ok....")
        
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
    

    
    def findPortfolioByStockCode(self, portfolio):
        ''' return as json 
        <th>股票代码</th>
        <th>股票名称</th>
        <th>持股数量</th>
        <th>最新价</th>
        <th>昨收</th>
        <th>今开</th>
        <th>成交量</th>
        <th>成交额</th>
        <th>持仓成本</th>
        <th>持仓市值</th>
        <th>盈亏</th>
        <th>盈亏百分比</th>
        '''
        df = ts.get_realtime_quotes(portfolio["stock_code"])
        
        #TODO for fututure should use transcation table to calc qty and cost
        
        market_value = int(portfolio["qty"]) * float(df.iloc[0]["price"])
        cost_amount = int(portfolio["qty"]) * float(portfolio["cost"])
        profit_lost = market_value - cost_amount
        precentage = "{percent:.2%}".format(percent=profit_lost/cost_amount)
        portfolioItem = {
            "_id":str(portfolio["_id"]), 
            "stock_code":portfolio["stock_code"], 
            "stock_name":portfolio["stock_name"], 
            "qty":portfolio["qty"], 
            "price":df.iloc[0]["price"], 
            "pre_close":df.iloc[0]["pre_close"], 
            "open_price":df.iloc[0]["open"], 
            "volume":df.iloc[0]["volume"], 
            "amount":df.iloc[0]["amount"], 
            "cost":portfolio["cost"], 
            "market_value":market_value, 
            "profit_lost":profit_lost, 
            "precentage":precentage
            }
        return portfolioItem

    def getPortfolios(self, user):
        log.info("trying to get portfolio list user : %s ", user)
        try:
            portfolios = self.db.portfolios.find({"userid":user.id})
            portfolioList = []
            for portfolio in portfolios:
                portfolioItem = self.findPortfolioByStockCode(portfolio)
                portfolioList.append(portfolioItem)
        except Exception as e:
            log.error(e)

        #datatable need data object
        return json.dumps({ "data" : portfolioList })
    
    
    def addPortfolio(self, user, newPortfolio):
        log.info("trying to add portfolio to data: %s", newPortfolio)
        
        try:
            newPortfolio["userid"] = user.id 
            self.db.portfolios.insert(newPortfolio)
            portfolioWithMarketData = self.findPortfolioByStockCode(newPortfolio)
            log.info(portfolioWithMarketData)
        except Exception as e:
            log.error(e)
        
        return json.dumps(portfolioWithMarketData)

    
    def deletePortfolios(self, user, ids):
        log.info("trying to delete portfolio list user : %s ", user)
        log.info("ids : %s ", ids)
        try:
            for objId in ids.split(","):
                if (objId != ""):
                    self.db.portfolios.delete_one({"_id": ObjectId(objId)})
        except Exception as e:
            log.error(e)
            json.dumps("failed")
        return json.dumps("success")
    
    def getStocks(self, market="all", date=None):
        log.info("getStocks market is %s", market)
        if (date == None):
            yesterday = datetime.datetime.now() - datetime.timedelta(days = 1)
            datestr = yesterday.strftime("%Y-%m-%d")
        else:
            datestr = date
            
        try:
            #TODO handle different market
            if (market == "all"):
                stocks = self.db.stocks.find({"load_date":datestr}, { "stock_code" : 1, "name":1,"_id" : 0 })
            elif (market == "sh"):
                stocks = self.db.stocks.find({"load_date":datestr}, { "stock_code" : 1, "name":1,"_id" : 0 })
            elif (market == "zh"):
                stocks = self.db.stocks.find({"load_date":datestr}, { "stock_code" : 1, "name":1,"_id" : 0 })
            else:
                stocks = []
                   
            stocksList = []
            for stock in stocks:
                #print stock
                stockItem = {  
                               "stock_code":stock["stock_code"],
                               "name":stock["name"]
                            }
                '''
                stockItem = {  "load_date":stock["load_date"],
                               "stock_code":stock["stock_code"],
                               "name":stock["name"],
                               "industry":stock["industry"],
                               "area":stock["area"],
                               "pe":stock["pe"],
                               "outstanding":stock["outstanding"],
                               "totals":stock["totals"],
                               "totalAssets":stock["totalAssets"],
                               "liquidAssets":stock["liquidAssets"],
                               "fixedAssets":stock["fixedAssets"],
                               "reserved":stock["reserved"],
                               "reservedPerShare":stock["reservedPerShare"],
                               "esp":stock["esp"],
                               "bvps":stock["bvps"],
                               "pb":stock["pb"],
                               "timeToMarket":stock["timeToMarket"],
                               "undp":stock["undp"],
                               "perundp":stock["perundp"],
                               "rev":stock["rev"],
                               "profit":stock["profit"],
                               "gpr":stock["gpr"],
                               "npr":stock["npr"],
                               "holders":stock["holders"]
                            }
                '''
                stocksList.append(stockItem)
        except Exception as e:
            log.error(e)
        return json.dumps(stocksList)