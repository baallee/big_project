from flask import request,make_response,render_template
from weixin import WeixinLogin
from datetime import datetime, timedelta
from DatabaseManager import DatabaseManager
from flask_login import login_user
import hashlib,time
import xml.etree.ElementTree as ET
import logging
from User import User




wxlogin = WeixinLogin('wx78ff74a2f031e715', '76b6e8235ff5febbbdedbb52e2a6183c')
log = logging.getLogger("SecurityManager")

db = DatabaseManager().db


def handleWechatLogin():
    try:
        code = request.args.get("code")
        state = request.args.get("state")
        log.info("request code:" + code)
        log.info("request state:" + state)
        if not code:
            return "ERR_INVALID_CODE", 400
        
        data = wxlogin.access_token(code)
        log.info(data)
        userinfo = wxlogin.user_info(data.access_token, data.openid)
        log.info(userinfo)
        
        mogouser = db.users.find_one({"openid":userinfo.openid})
        user = None
        #check wechat user authorized
        if mogouser == None:
            db.users.insert({"openid":userinfo.openid, "nickname":userinfo.nickname, "sex":userinfo.nickname, "language": userinfo.language, 
                            "city": userinfo.city, "province": userinfo.province, "country": userinfo.country, "headimgurl": userinfo.headimgurl})
            #for first time wechat authorized 
            user = User(db.users.find_one({"openid":userinfo.openid}))
        else:
            user = User(mogouser)
        
        login_user(user)
        resp = make_response(render_template('index.html', user=user))
        expires = datetime.now() + timedelta(days=1)
        openid = data.openid
        resp.set_cookie("openid", openid, expires=expires)
        return resp
    except Exception as e:
        log.error(e)
        return "Internal Server Error", 500
    else:
        return "Unknow Error", 500

def wechatAuth():
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