import datetime
import logging
import SecurityManager as sm
from pymongo import MongoClient
from flask import Flask,render_template,json


logger = logging.getLogger('big_project')
hdlr = logging.FileHandler('logs/web.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
logger.setLevel(logging.WARNING)


app = Flask(__name__)
client = MongoClient('localhost', 27017)
db = client.big_project

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login.html')
def logout():
    return render_template('login.html')


@app.route('/index.html')
def index():
    
    return render_template('index.html')

@app.route('/tables.html')
def tables():
    return render_template('tables.html')

@app.route('/flot.html')
def flot():
    return render_template('flot.html')

@app.route('/morris.html')
def morris():
    return render_template('morris.html')

@app.route('/forms.html')
def forms():
    return render_template('forms.html')

@app.route('/panels-wells.html')
def panelsWells():
    return render_template('panels-wells.html')

@app.route('/buttons.html')
def buttons():
    return render_template('buttons.html')

@app.route('/notifications.html')
def notifications():
    return render_template('notifications.html')

@app.route('/typography.html')
def typography():
    return render_template('typography.html')

@app.route('/icons.html')
def icons():
    return render_template('icons.html')

@app.route('/grid.html')
def grid():
    return render_template('grid.html')

@app.route('/stocks.html')
def stocks():
    return render_template('stocks.html')

@app.route('/dashboard.html')
def dashboard():
    return render_template('dashboard.html')

@app.route("/authorized")
def authorized():
    return sm.handleLogin()

@app.route('/wxlogin',methods=['GET','POST'])
def wechat_auth():
    return sm.wechatAuth()

@app.route('/getStockList', methods=['POST'])
def getStockList():
    yesterday = datetime.datetime.now() - datetime.timedelta(days = 1)
    datestr = yesterday.strftime("%Y-%m-%d")
    logger.info("trying to get stocks list at date : " + datestr)
    
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
    except Exception as e:
        logging.error(e)
        return str(e)
    return json.dumps(stocksList)


if __name__ == '__main__':
    app.run()
