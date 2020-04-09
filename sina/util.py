# -*- coding: utf-8 -*-


import hashlib,datetime,re,demjson
import pymysql
import requests

class mysqlObj(object):
    
    def __init__(self):
        self.connect = pymysql.connect(
            host= "127.0.0.1",
            db="huanqiu",
            user="root",
            passwd="123456",
            charset='utf8mb4',
            use_unicode=True,
            cursorclass=pymysql.cursors.DictCursor
        )
        
    def request_add_or_update(self, linkA):
        self.connect.ping(reconnect=True)
        cursor = self.connect.cursor()
        currentDT = datetime.datetime.now()
        currentDTStr = currentDT.strftime("%Y-%m-%d %H:%M:%S")
        o = hashlib.md5(linkA.encode("utf8")).hexdigest()
        #檢查requests表
        cursor.execute("""SELECT * from tb_request where id = %s""", o)
        resultR = cursor.fetchone()
        if resultR:
            cursor.execute("""update tb_request set status=1 , update_time=%s where id = %s """,    
                (currentDTStr,o))
            self.connect.commit()
        else:
            cursor.execute(
                """insert into tb_request( id,url,status,create_time,update_time
                )value ( %s,%s,1,%s,%s )""",
                ( o, linkA, currentDTStr,currentDTStr ))
            self.connect.commit()
            
    def request_add(self, linkA):
        cursor = self.connect.cursor()
        currentDT = datetime.datetime.now()
        currentDTStr = currentDT.strftime("%Y-%m-%d %H:%M:%S")
        m = hashlib.md5(linkA.encode("utf8")).hexdigest()
        cursor.execute("""SELECT * from tb_request where id = %s""", m)
        result = cursor.fetchone()
        if not result:
                cursor.execute(
                    """insert into tb_request( id,url,status,create_time
                    ) value ( %s,%s,0,%s )""",
                    ( m, linkA, currentDTStr ))
                self.connect.commit()
                return 1
        elif result.get('status') == 0:
            return 2
        else:
            return 0
    
class myUtil(object):
    
    DATEObject2020 = datetime.datetime.strptime("2020-01-01 00:00", "%Y-%m-%d %H:%M")
    TIMESTAMPStr2020 = '1577808000'
    TIMESTAMPInt2020 = 1577808000000
    DATEObjectNow = datetime.datetime.now()
#     req = requests
    req = requests.Session()
    def myip(self):
        r = self.req.get('http://106.75.48.143/task/ip42')
        ip = r.text
        if re.match('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', ip) == None:
            ip = None
        return ip
    
    def myJsonp(self,jsonpStr):
        jsonStr = re.match(r'.*?({.*}).*', jsonpStr, re.S).group(1)
        return demjson.decode(jsonStr)
    
    def daysAgo(self,dateA,d):
        if self.DATEObjectNow - datetime.timedelta(days=d) < dateA and dateA - datetime.timedelta(days=d) < self.DATEObjectNow:
            return True
        return False
    
    def stringToDict(self,cookieStr):
        cookieItemDict = {}
        cookieItems = cookieStr.split(';')
        for cookieItem in cookieItems:
            key = cookieItem.split('=')[0].replace(' ', '')
            value = cookieItem.split('=')[1]
            cookieItemDict[key] = value
        return cookieItemDict
#     def myGetRequest(self,link):
#         jsonStr = re.match(r'.*?({.*}).*', jsonpStr, re.S).group(1)
#         return demjson.decode(jsonStr)
    
    