
import logUtils,logging
import SecurityManager as sm
from User import User
from DatabaseManager import DatabaseManager 
from flask import Flask,render_template,json,request,make_response
from flask_login import LoginManager,login_required,login_user,logout_user,current_user


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

@app.route('/portfolios')
@login_required
def getPortfolios():
    return dbMgr.getPortfolios(current_user)


if __name__ == '__main__':
    app.run()
