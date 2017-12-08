from flask import Flask,request,render_template,make_response
import time
import hashlib
import xml.etree.ElementTree as ET

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

@app.route('/wxlogin',methods=['GET','POST'])
def wechat_auth():
    if request.method == 'GET':
        token='big_project' #your token
        data = request.args
        signature = data.get('signature','')
        timestamp = data.get('timestamp','')
        nonce = data.get('nonce','')
        echostr = data.get('echostr','')
        s = [timestamp,nonce,token]
        s.sort()
        s = ''.join(s)
        if (hashlib.sha1(s.encode(encoding='utf_8', errors='strict')).hexdigest() == signature):
            return make_response(echostr)
    else:
        rec = request.stream.read()
        xml_rec = ET.fromstring(rec)
        tou = xml_rec.find('ToUserName').text
        fromu = xml_rec.find('FromUserName').text
        content = xml_rec.find('Content').text
        xml_rep = "<xml><ToUserName><![CDATA[%s]]></ToUserName><FromUserName><![CDATA[%s]]></FromUserName><CreateTime>%s</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[%s]]></Content><FuncFlag>0</FuncFlag></xml>"
        response = make_response(xml_rep % (fromu,tou,str(int(time.time())), content))
        response.content_type='application/xml'
        return response
    return 'Hello weixin!'

if __name__ == '__main__':
    app.run()
