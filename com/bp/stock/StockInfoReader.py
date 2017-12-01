'''
@author: Baal
'''
import tushare as ts
import datetime
import pandas as pd
import json


from pymongo import MongoClient
from openpyxl import load_workbook
from numpy import empty

def getStockCode(row):
    return row.name

yesterday = datetime.datetime.now() - datetime.timedelta(days = 1)
datestr = yesterday.strftime("%Y-%m-%d")
fileName = "/Users/Baal/Desktop/Projects/Big_Project/Stock_full_closing_info_" +  datestr + ".xlsx"

sd = ts.get_stock_basics()

sd = sd.assign(load_date=datestr)
sd['stock_code'] = sd.apply(getStockCode, axis=1)
sd.to_excel(fileName,sheet_name="stock_list",encoding="utf-8")

conn = MongoClient('localhost', 27017)

conn.big_project.stocks.remove({"load_date" : datestr})
conn.big_project.hist_data.remove({"load_date" : datestr})

conn.big_project.stocks.insert(json.loads(sd.to_json(orient='records')))

book = load_workbook(fileName)
writer = pd.ExcelWriter(fileName, engine='openpyxl') 
writer.book = book

#level 1 strategy
#sd = sd[(sd.pe <= 20) & (sd.pe > 0) & (sd.totalAssets <= 200000)]

header = pd.DataFrame(columns=["open","high","close","low","volume","price_change","p_change",
                               "ma5","ma10","ma20","v_ma5","v_ma10","v_ma20","turnover",
                               "stock_code","load_date"])

header.to_excel(writer, sheet_name="closing_info", startrow=0, index=False)

i = 1
for code in sd.index:
    #TODO level 2 strategy
    try:
        p = ts.get_hist_data(code, start=datestr, end=datestr, retry_count=10)
        p = p.assign(stock_code=code)
        p = p.assign(load_date=datestr)
    except BaseException:
        print "error"
    else:
        if not p.empty:
            print(p)
            p.to_excel(writer, sheet_name="closing_info", startrow=i, index=False, header=False)
            conn.big_project.hist_data.insert(json.loads(p.to_json(orient='records')))
            i = i + 1

writer.save()