from flask import request,redirect,make_response
from weixin import WeixinLogin
from datetime import datetime, timedelta
import hashlib,time
import logUtils
import xml.etree.ElementTree as ET

wxlogin = WeixinLogin('wx78ff74a2f031e715', '76b6e8235ff5febbbdedbb52e2a6183c')
log = logUtils.getLogger()

def handleLogin():
    try:
        code = request.args.get("code")
        if not code:
            return "ERR_INVALID_CODE", 400
        
        data = wxlogin.access_token(code)
        log.info(data)
        openid = data.openid
        resp = redirect("index.html")
        expires = datetime.now() + timedelta(days=1)
        resp.set_cookie("openid", openid, expires=expires)
    except Exception as e:
        log.error(e)
    else:
        return resp

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