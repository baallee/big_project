'''
@author: Baal
'''

import datetime
from flask import Flask, render_template,jsonify,json,request
from pymongo import MongoClient

application = Flask(__name__)

yesterday = datetime.datetime.now() - datetime.timedelta(days = 1)
datestr = yesterday.strftime("%Y-%m-%d")

client = MongoClient('localhost', 27017)
db = client.big_project

@application.route('/')
def showMachineList():
    return render_template('list.html')


@application.route('/addMachine', methods=['POST'])
def addMachine():
    try:
        json_data = request.json['info']
        deviceName = json_data['device']
        ipAddress = json_data['ip']
        userName = json_data['username']
        password = json_data['password']
        portNumber = json_data['port']
        
        db.Machines.insert_one({'device': deviceName, 'ip': ipAddress,
                                'username': userName, 'password': password,
                                'port': portNumber})
        return jsonify(status='OK', message='inserted success')
    except Exception, e:
        print e
        return jsonify(status='ERROR', message=str(e))
    

@application.route('/getStockList', methods=['POST'])
def getStockList():
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
    except Exception, e:
        print e
        return str(e)
    return json.dumps(stocksList)


if __name__ == "__main__":
    application.run(host='0.0.0.0')