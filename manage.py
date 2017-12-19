import logUtils,logging
import SecurityManager as sm
from DatabaseManager import DatabaseManager 
from apscheduler.schedulers.blocking import BlockingScheduler
from flask import Flask,render_template,json,request,make_response
from flask_login import LoginManager,login_required,login_user,logout_user,current_user
from StockInfoReader import stockInfoDailyJob


#init logging module
logUtils.init()

log = logging.getLogger("manager")
log.info("server starting....")

dbMgr = DatabaseManager()

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
    return dbMgr.findUserByOpenId(openid)

###################handle user login start####################

@app.route('/')
def landing():
    return render_template('login.html')

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        #load user from users table using username    
        user = dbMgr.findUserByName(username)
        #TODO password hardcode
        if user is not None and password == "pass1234":
            login_user(user)
            return render_template('index.html', user=user, stocks=dbMgr.getStocks(market="all"))
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

###################handle user login end####################

###################page routing start####################

@app.route('/main.html')
def main_html():
    return render_template('demo/main.html')

@app.route('/tables.html')
def tables_html():
    return render_template('demo/tables.html')

@app.route('/flot.html')
def flot_html():
    return render_template('demo/flot.html')

@app.route('/morris.html')
def morris_html():
    return render_template('demo/morris.html')

@app.route('/forms.html')
def forms_html():
    return render_template('demo/forms.html')

@app.route('/panels-wells.html')
def panelsWells_html():
    return render_template('demo/panels-wells.html')

@app.route('/buttons.html')
def buttons_html():
    return render_template('demo/buttons.html')

@app.route('/notifications.html')
def notifications_html():
    return render_template('demo/notifications.html')

@app.route('/typography.html')
def typography_html():
    return render_template('demo/typography.html')

@app.route('/icons.html')
def icons_html():
    return render_template('demo/icons.html')

@app.route('/grid.html')
def grid_html():
    return render_template('demo/grid.html')

@app.route('/dashboard.html')
def dashboard():
    return render_template('demo/dashboard.html')

@app.route('/index.html')
@login_required
def index_html():
    return render_template('index.html')

@app.route('/portfolio.html')
@login_required
def portfolio_html():
    return render_template('portfolio.html')

@app.route('/strategy.html')
@login_required
def strategy_html():
    return render_template('strategy.html')

###################page routing end####################

###################business logic start##################

@app.route('/wxlogin',methods=['GET','POST'])
def wechat_auth():
    return sm.wechatAuth()

@app.route('/portfolios', methods=['GET'])
@login_required
def getPortfolios():
    return dbMgr.getPortfolios(current_user)
    #for testing
    #return  current_app.send_static_file('data/portfolios.js')


@app.route('/portfolio/add', methods=['POST'])
@login_required
def addPortfolio():
    dataDict = json.loads(request.data)
    log.info(dataDict)
    data = dbMgr.addPortfolio(current_user, dataDict)
    return data


@app.route('/portfolio/delete', methods=['POST'])
@login_required
def delPortfolio():
    ids = json.loads(request.data)
    data = dbMgr.deletePortfolios(current_user, ids)
    return data

@app.route('/stocks/<market>')
@login_required
def getStocksForSelect(market):
    log.info(market)
    return dbMgr.getStocks(market=market)


##################business logic start##################

# BlockingScheduler
scheduler = BlockingScheduler()
#scheduler.add_job(job, 'cron', day_of_week='1-5', hour=6, minute=30)
scheduler.add_job(stockInfoDailyJob, 'cron', day_of_week='1-6', hour="*", minute="*")
scheduler.start()


if __name__ == '__main__':
    app.run()
