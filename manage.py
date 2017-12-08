import web  
from flask import Flask, render_template

app = Flask(__name__)


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

@app.route('/wxlogin')
def wxlogin():
    try:  
        data = web.input()  
        if len(data) == 0:  
            return "could not get request"  
        signature = data.signature  
        timestamp = data.timestamp  
        nonce = data.nonce  
        echostr = data.echostr  
        token = "big_project"  
        list = [token, timestamp, nonce]  
        list.sort()  
        sha1 = hashlib.sha1()  
        map(sha1.update, list)  
        hashcode = sha1.hexdigest()  
        print "handle/GET func: hashcode, signature: ", hashcode, signature  
        if hashcode == signature:  
            return echostr  
        else:  
            return ""  
    except Exception, Argument:  
        return Argument 

if __name__ == '__main__':
    app.run()
