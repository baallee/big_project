import datetime
import logUtils,logging
import SecurityManager as sm
from User import User
from DatabaseManager import DatabaseManager 
from flask import Flask,render_template,json,request,make_response
from flask_login import LoginManager,login_required,login_user,logout_user 


#init logging module
logUtils.init()

log = logging.getLogger("manager")
log.info("server starting....")

db = DatabaseManager().db

#init web server
app = Flask(__name__)
# config
app.config.update(
    DEBUG = True,
    SECRET_KEY = 'secret_login'
)


# flask-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
    

# callback to reload the user object        
@login_manager.user_loader
def load_user(openid):
    if (db.users.find_one({"openid":openid}) == None):
        return None
    else:
        userinfo = db.users.find_one({"openid":openid})
        return User(userinfo)

@app.route('/')
def landing():
    return render_template('login.html')

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        #load user from users table using username    
        mogouser = db.users.find_one({"nickname":username})
        #TODO password hardcode
        if mogouser is not None and password == "pass1234":
            user = User(mogouser)
            login_user(user)
            return render_template('index.html', user=user)
        else:
            return make_response(render_template('login.html', errorcode=401, errormessage="Username or password are not correct."))
    else:
        return render_template('login.html')
    
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('login.html')

@app.route("/authorized")
def authorized():
    return sm.handleWechatLogin()

@app.route('/index.html')
@login_required
def index():
    return render_template('index.html')

@app.route('/tables.html')
@login_required
def tables():
    return render_template('tables.html')

@app.route('/flot.html')
@login_required
def flot():
    return render_template('flot.html')

@app.route('/morris.html')
@login_required
def morris():
    return render_template('morris.html')

@app.route('/forms.html')
@login_required
def forms():
    return render_template('forms.html')

@app.route('/panels-wells.html')
@login_required
def panelsWells():
    return render_template('panels-wells.html')

@app.route('/buttons.html')
@login_required
def buttons():
    return render_template('buttons.html')

@app.route('/notifications.html')
@login_required
def notifications():
    return render_template('notifications.html')

@app.route('/typography.html')
@login_required
def typography():
    return render_template('typography.html')

@app.route('/icons.html')
@login_required
def icons():
    return render_template('icons.html')

@app.route('/grid.html')
@login_required
def grid():
    return render_template('grid.html')

@app.route('/stocks.html')
@login_required
def stocks():
    return render_template('stocks.html')

@app.route('/dashboard.html')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/wxlogin',methods=['GET','POST'])
def wechat_auth():
    return sm.wechatAuth()

@app.route('/getStockList', methods=['POST'])
@login_required
def getStockList():
    yesterday = datetime.datetime.now() - datetime.timedelta(days = 1)
    datestr = yesterday.strftime("%Y-%m-%d")
    log.info("trying to get stocks list at date : " + datestr)
    
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
        log.error(e)
        return str(e)
    return json.dumps(stocksList)


if __name__ == '__main__':
    app.run()
