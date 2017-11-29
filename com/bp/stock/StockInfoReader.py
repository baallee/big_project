'''
@author: Baal
'''
import tushare as ts
import datetime
import numpy as np
import pandas as pd
from openpyxl import load_workbook

yesterday = datetime.datetime.now() #- datetime.timedelta(days = 1)
datestr = yesterday.strftime("%Y-%m-%d")
fileName = "/Users/Baal/Desktop/Projects/Big_Project/Stock_full_closing_info_" +  datestr + ".xlsx"

sd = ts.get_stock_basics()
sd.to_excel(fileName,sheet_name="stock_list",encoding="utf-8")

book = load_workbook(fileName)
writer = pd.ExcelWriter(fileName, engine='openpyxl') 
writer.book = book

#sd = sd[0:10]
header = pd.DataFrame(columns=["open","high","close","low","volume","price_change","p_change","ma5","ma10","ma20","v_ma5","v_ma10","v_ma20","turnover","stock_code"])
header.to_excel(writer, sheet_name="closing_info", startrow=0, index=False)
i = 1
for code in sd.index:
    print(i)
    p = ts.get_hist_data(code, start=datestr, end=datestr, retry_count=10)
    p = p.assign(stock_code=code)
    print(p)
    p.to_excel(writer, sheet_name="closing_info", startrow=i, index=False, header=False)
    i = i + 1

writer.save()