'''
Created on 2017年12月13日

@author: Baal
'''
from flask_login.mixins import UserMixin

class User(UserMixin):

    def __init__(self, userinfo):
        self.id = userinfo["openid"]
        
        self.name = userinfo["nickname"]
        self.sex = userinfo["sex"]
        self.language = userinfo["language"]
        self.city = userinfo["city"]
        self.province = userinfo["province"]
        self.country = userinfo["country"]
        self.headimgurl = userinfo["headimgurl"]
        #TODO
        self.password = "pass1234"
        
    def __repr__(self):
        return "%d/%s/%s" % (self.id, self.name, self.password)