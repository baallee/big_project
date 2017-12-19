'''
@author: Baal
'''
import tushare as ts
import pandas as pd
import json
import logging
from openpyxl import load_workbook
import datetime
from DatabaseManager import DatabaseManager

log = logging.getLogger("StockInfoReader")
db = DatabaseManager().db
    
def getStockCode(row):
    return row.name

def stockInfoDailyJob():
    log.info("job started......")
    yesterday = datetime.datetime.now() - datetime.timedelta(days = 1)
    datestr = yesterday.strftime("%Y-%m-%d")
    fileName = "/home/ubuntu/dev/big_project/outputs/Stock_full_closing_info_" +  datestr + ".xlsx"
    
    sd = ts.get_stock_basics()
    
    sd = sd.assign(load_date=datestr)
    sd['stock_code'] = sd.apply(getStockCode, axis=1)
    sd.to_excel(fileName,sheet_name="stock_list",encoding="utf-8")
    
    conn = db
    
    conn.stocks.remove({"load_date" : datestr})
    conn.hist_data.remove({"load_date" : datestr})
    
    conn.stocks.insert(json.loads(sd.to_json(orient='records')))
    
    book = load_workbook(fileName)
    writer = pd.ExcelWriter(fileName, engine='openpyxl') 
    writer.book = book
    
    header = pd.DataFrame(columns=["open","high","close","low","volume","price_change","p_change",
                                   "ma5","ma10","ma20","v_ma5","v_ma10","v_ma20","turnover",
                                   "stock_code","load_date"])
    
    header.to_excel(writer, sheet_name="closing_info", startrow=0, index=False)
    
    i = 1
    for code in sd.index:
        try:
            p = ts.get_hist_data(code, start=datestr, end=datestr, retry_count=10)
            p = p.assign(stock_code=code)
            p = p.assign(load_date=datestr)
        except:
            log.error("unknow error")
        else:
            if not p.empty:
                p.to_excel(writer, sheet_name="closing_info", startrow=i, index=False, header=False)
                conn.hist_data.insert(json.loads(p.to_json(orient='records')))
                i = i + 1
    
    writer.save()

    #update load_date in sys_prop
    prop = conn.sys_prop.find_one({"prop_name":"load_date"})
    if (prop == None):
        conn.sys_prop.insert({"prop_name":"load_date", "prop_value":datestr})
    else:
        conn.sys_prop.update_one({"prop_name":"load_date"}, {"$set" : {"prop_value": datestr}}, upsert=False)
    
    log.info("job finished.............") 